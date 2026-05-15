import curses

from .editor import FilterEditor
from .lessons import load_all
from .progress import InMemoryProgress, Progress
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
                self.run_filter()
                return False
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
                return False
            if ch.isprintable():
                self.editor.insert(ch)
                return False
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
        if ch == curses.KEY_RESIZE:
            return False
        return False

    def run_filter(self) -> None:
        text = self.editor.text.strip()
        if not text:
            cmd = self.editor.text
            if cmd in ("q", "quit", ":q"):
                raise SystemExit(0)
            return
        if text == "q" or text == ":q" or text == "quit":
            raise SystemExit(0)
        if text == "n":
            self._command_next()
            return
        if text == "p":
            self._command_prev()
            return
        if text == "h":
            self.show_hint = not self.show_hint
            self.editor.reset()
            return
        if text == "s":
            self.show_expected = not self.show_expected
            self.editor.reset()
            return
        if text == "r":
            self.editor.reset()
            self.status = ""
            self.got_text = ""
            return
        if text == "j":
            self.scroll += 1
            self.editor.reset()
            return
        if text == "k":
            self.scroll = max(0, self.scroll - 1)
            self.editor.reset()
            return

        result = validate(text, self.lesson.input_json, self.lesson.expected_outputs)
        self.got_text = result.got_text
        if result.error:
            self.status = f"[ERROR] {result.error}"
        elif result.passed:
            self.status = "[PASS]  Press 'n' (then Enter) to advance."
            self.show_expected = True
            self.current_passed = True
            self.progress.mark_passed(self.lesson.id)
        else:
            self.status = "[FAIL]  Output does not match expected. Try 'h' for a hint or 's' to reveal."
        self.scroll = 0

    def _command_next(self) -> None:
        if not self.current_passed and not self.progress.is_passed(self.lesson.id):
            self.editor.reset()
            self.status = "[FAIL]  Solve the current lesson first."
            return
        if self.lesson_idx + 1 < len(self.stage.lessons):
            self.lesson_idx += 1
        elif self.stage_idx + 1 < len(self.stages):
            self.stage_idx += 1
            self.lesson_idx = 0
        else:
            self.editor.reset()
            self.status = "[PASS]  Course complete. Press q to quit."
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
    progress = InMemoryProgress()

    def _entry(stdscr):
        App(stdscr, progress).run()

    try:
        curses.wrapper(_entry)
    except SystemExit:
        pass
    return 0
