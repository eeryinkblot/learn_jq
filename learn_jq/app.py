import argparse
import curses

from .editor import FilterEditor
from .lessons import load_all
from .progress import InMemoryProgress, JsonFileProgress, Progress, default_progress_path
from .ui import Renderer
from .validator import validate


class App:
    def __init__(self, stdscr, progress: Progress) -> None:
        self.stdscr = stdscr
        self.stages = load_all()
        self.progress = progress
        self.renderer = Renderer(stdscr)
        self.editor = FilterEditor()
        self.stage_idx = 0
        self.lesson_idx = 0
        self.status = ""
        self.got_text = ""
        self.scroll = 0
        self.show_hint = False
        self.show_expected = False
        self.current_passed = False
        self._resume_to_first_unpassed()

    def _resume_to_first_unpassed(self) -> None:
        for si, stage in enumerate(self.stages):
            for li, lesson in enumerate(stage.lessons):
                if not self.progress.is_passed(lesson.id):
                    self.stage_idx = si
                    self.lesson_idx = li
                    return
        self.stage_idx = len(self.stages) - 1
        self.lesson_idx = len(self.stages[-1].lessons) - 1

    @property
    def stage(self):
        return self.stages[self.stage_idx]

    @property
    def lesson(self):
        return self.stage.lessons[self.lesson_idx]

    def load_lesson_state(self) -> None:
        self.editor.reset()
        self.status = ""
        self.got_text = ""
        self.scroll = 0
        self.show_hint = False
        self.show_expected = False
        self.current_passed = self.progress.is_passed(self.lesson.id)

    def run(self) -> None:
        curses.curs_set(1)
        self.stdscr.keypad(True)
        try:
            self.stdscr.notimeout(False)
            curses.set_escdelay(25)
        except (AttributeError, curses.error):
            pass
        self.load_lesson_state()
        self.draw()
        while True:
            try:
                ch = self.stdscr.get_wch()
            except curses.error:
                continue
            except KeyboardInterrupt:
                break
            if self._dispatch(ch):
                break
            self.draw()

    def _dispatch(self, ch) -> bool:
        if isinstance(ch, str):
            if ch in ("\n", "\r"):
                self._on_enter()
                return False
            if ch == "\t":
                self._command_next()
                return False
            if ch == "\x1b":
                return True
            if ch == "\x7f" or ch == "\b":
                self.editor.backspace()
                return False
            if ch == "\x01":
                self.editor.home()
                return False
            if ch == "\x05":
                self.editor.end()
                return False
            if ch == "\x15":
                self.editor.reset()
                self.status = ""
                return False
            if ch.isprintable():
                self.editor.insert(ch)
                return False
            return False
        if ch == curses.KEY_ENTER:
            self._on_enter()
            return False
        if ch == curses.KEY_BACKSPACE:
            self.editor.backspace()
            return False
        if ch == curses.KEY_DC:
            self.editor.delete()
            return False
        if ch == curses.KEY_LEFT:
            self.editor.left()
            return False
        if ch == curses.KEY_RIGHT:
            self.editor.right()
            return False
        if ch == curses.KEY_HOME:
            self.editor.home()
            return False
        if ch == curses.KEY_END:
            self.editor.end()
            return False
        if ch == curses.KEY_BTAB:
            self._command_prev()
            return False
        if ch == curses.KEY_F1:
            self.show_hint = not self.show_hint
            return False
        if ch == curses.KEY_F2:
            self.show_expected = not self.show_expected
            return False
        if ch == curses.KEY_F3:
            self._command_prev()
            return False
        if ch == curses.KEY_NPAGE:
            self.scroll += 5
            return False
        if ch == curses.KEY_PPAGE:
            self.scroll = max(0, self.scroll - 5)
            return False
        if ch == curses.KEY_RESIZE:
            return False
        return False

    def _on_enter(self) -> None:
        text = self.editor.text.strip()
        if not text:
            if self.current_passed:
                self._command_next()
            return
        self._evaluate(text)

    def _evaluate(self, text: str) -> None:
        result = validate(text, self.lesson.input_json, self.lesson.expected_outputs)
        self.got_text = result.got_text
        if result.error:
            self.status = f"[ERROR] {result.error}"
        elif result.passed:
            self.status = "[PASS]  Tab to advance (or Enter on empty filter)."
            self.show_expected = True
            self.current_passed = True
            self.progress.mark_passed(self.lesson.id)
        else:
            self.status = "[FAIL]  Output does not match. F1 for hint, F2 to reveal."
        self.scroll = 0

    def _command_next(self) -> None:
        if not self.current_passed and not self.progress.is_passed(self.lesson.id):
            self.status = "[FAIL]  Solve the current lesson before advancing."
            return
        if self.lesson_idx + 1 < len(self.stage.lessons):
            self.lesson_idx += 1
        elif self.stage_idx + 1 < len(self.stages):
            self.stage_idx += 1
            self.lesson_idx = 0
        else:
            self.status = "[PASS]  Course complete. Esc to quit."
            return
        self.load_lesson_state()

    def _command_prev(self) -> None:
        if self.lesson_idx > 0:
            self.lesson_idx -= 1
        elif self.stage_idx > 0:
            self.stage_idx -= 1
            self.lesson_idx = len(self.stages[self.stage_idx].lessons) - 1
        else:
            return
        self.load_lesson_state()

    def draw(self) -> None:
        self.renderer.draw(
            stage=self.stage,
            lesson=self.lesson,
            lesson_idx_in_stage=self.lesson_idx,
            editor_text=self.editor.text,
            editor_cursor=self.editor.cursor,
            status=self.status,
            got_text=self.got_text,
            scroll=self.scroll,
            progress=self.progress,
            show_hint=self.show_hint,
            show_expected=self.show_expected,
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="learn_jq",
        description="A terminal course for learning jq.",
    )
    parser.add_argument(
        "--in-memory",
        action="store_true",
        help="Do not persist progress to disk. Default is to save to ~/.local/share/learn_jq/progress.json.",
    )
    parser.add_argument(
        "--progress-file",
        metavar="PATH",
        default=None,
        help="Path to the progress file. Overrides the default location.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete saved progress before starting.",
    )
    args = parser.parse_args()

    if args.in_memory:
        progress: Progress = InMemoryProgress()
        progress_path_msg = "in-memory (not persisted)"
    else:
        from pathlib import Path

        path = Path(args.progress_file) if args.progress_file else default_progress_path()
        if args.reset and path.exists():
            path.unlink()
        progress = JsonFileProgress(path)
        progress_path_msg = str(path)

    def _entry(stdscr):
        App(stdscr, progress).run()

    try:
        curses.wrapper(_entry)
    except SystemExit:
        pass
    print(f"Progress: {progress_path_msg}")
    return 0
