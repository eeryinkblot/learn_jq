import curses
import json
import textwrap

from .models import Lesson, Stage
from .progress import Progress


MIN_COLS = 60
MIN_ROWS = 20


def pretty(json_text: str) -> str:
    try:
        return json.dumps(json.loads(json_text), indent=2)
    except json.JSONDecodeError:
        return json_text


def wrap_lines(text: str, width: int) -> list[str]:
    out: list[str] = []
    for line in text.splitlines() or [""]:
        if not line:
            out.append("")
            continue
        out.extend(textwrap.wrap(line, width=width) or [""])
    return out


def truncate(line: str, width: int) -> str:
    if len(line) <= width:
        return line
    if width <= 1:
        return line[:width]
    return line[: width - 1] + ">"


def safe_addstr(win, y: int, x: int, s: str, attr: int = 0) -> None:
    try:
        win.addstr(y, x, s, attr)
    except curses.error:
        pass


class Renderer:
    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        self.use_color = curses.has_colors()
        if self.use_color:
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_CYAN, -1)
            curses.init_pair(2, curses.COLOR_GREEN, -1)
            curses.init_pair(3, curses.COLOR_RED, -1)
            curses.init_pair(4, curses.COLOR_YELLOW, -1)
        self.A_HEADER = (curses.color_pair(1) | curses.A_BOLD) if self.use_color else curses.A_BOLD
        self.A_PASS = (curses.color_pair(2) | curses.A_BOLD) if self.use_color else curses.A_BOLD
        self.A_FAIL = (curses.color_pair(3) | curses.A_BOLD) if self.use_color else curses.A_BOLD
        self.A_HINT = curses.color_pair(4) if self.use_color else curses.A_DIM

    def draw(
        self,
        stage: Stage,
        lesson: Lesson,
        lesson_idx_in_stage: int,
        editor_text: str,
        editor_cursor: int,
        status: str,
        got_text: str,
        scroll: int,
        progress: Progress,
        show_hint: bool,
        show_expected: bool,
    ) -> None:
        self.stdscr.erase()
        rows, cols = self.stdscr.getmaxyx()

        if cols < MIN_COLS or rows < MIN_ROWS:
            safe_addstr(self.stdscr, 0, 0, f"Window too small. Need at least {MIN_COLS}x{MIN_ROWS}.")
            self.stdscr.refresh()
            return

        passed_count = progress.passed_count([lson.id for lson in stage.lessons])
        header = (
            f"Stage {stage.number}/5: {stage.name} | "
            f"Lesson {lesson.id} ({lesson_idx_in_stage + 1}/{len(stage.lessons)}): {lesson.title} | "
            f"Stage progress: {passed_count}/{len(stage.lessons)}"
        )
        safe_addstr(self.stdscr, 0, 0, truncate(header, cols), self.A_HEADER)
        safe_addstr(self.stdscr, 1, 0, "-" * cols)

        desc_lines = wrap_lines(lesson.description, cols - 2)
        desc_top = 2
        desc_height = min(len(desc_lines), 5)
        for i in range(desc_height):
            safe_addstr(self.stdscr, desc_top + i, 1, desc_lines[i])

        if show_hint:
            hint_line = f"Hint: {lesson.hint}"
            safe_addstr(self.stdscr, desc_top + desc_height, 1, truncate(hint_line, cols - 2), self.A_HINT)
            desc_height += 1

        sep_row = desc_top + desc_height
        safe_addstr(self.stdscr, sep_row, 0, "-" * cols)

        editor_row = rows - 5
        output_top = sep_row + 1
        output_bottom = editor_row - 1
        pane_height = output_bottom - output_top

        if pane_height < 6:
            pane_height = 6
            output_bottom = output_top + pane_height
            editor_row = output_bottom + 1

        left_width = cols // 2 - 1
        right_width = cols - left_width - 1

        input_pretty = pretty(lesson.input_json)
        input_lines = input_pretty.splitlines()
        expected_lines = []
        if show_expected:
            for ex in lesson.expected_outputs:
                expected_lines.extend(pretty(ex).splitlines())
        else:
            expected_lines = ["(press 's' to reveal)"]

        input_pane_height = pane_height // 2
        output_pane_height = pane_height - input_pane_height - 1

        safe_addstr(self.stdscr, output_top, 0, "INPUT", self.A_HEADER)
        safe_addstr(self.stdscr, output_top, left_width + 1, "EXPECTED", self.A_HEADER)
        for i in range(input_pane_height - 1):
            li = input_lines[i] if i < len(input_lines) else ""
            ri = expected_lines[i] if i < len(expected_lines) else ""
            safe_addstr(self.stdscr, output_top + 1 + i, 0, truncate(li, left_width))
            safe_addstr(self.stdscr, output_top + 1 + i, left_width + 1, truncate(ri, right_width))
        for i in range(input_pane_height):
            safe_addstr(self.stdscr, output_top + i, left_width, "|")

        out_header_row = output_top + input_pane_height
        safe_addstr(self.stdscr, out_header_row, 0, "OUTPUT", self.A_HEADER)
        got_lines = got_text.splitlines() if got_text else ["(press Enter to run)"]
        visible_got = got_lines[scroll : scroll + output_pane_height]
        for i, gl in enumerate(visible_got):
            safe_addstr(self.stdscr, out_header_row + 1 + i, 0, truncate(gl, cols))

        safe_addstr(self.stdscr, editor_row, 0, "-" * cols)
        prompt = "FILTER> "
        safe_addstr(self.stdscr, editor_row + 1, 0, prompt, self.A_HEADER)
        avail = cols - len(prompt) - 1
        if avail < 1:
            avail = 1
        scroll_x = max(0, editor_cursor - avail + 1)
        visible_text = editor_text[scroll_x : scroll_x + avail]
        safe_addstr(self.stdscr, editor_row + 1, len(prompt), visible_text)

        status_row = editor_row + 2
        if status.startswith("[PASS"):
            attr = self.A_PASS
        elif status.startswith("[FAIL") or status.startswith("[ERROR"):
            attr = self.A_FAIL
        else:
            attr = curses.A_DIM
        safe_addstr(self.stdscr, status_row, 0, truncate(status, cols), attr)

        help_row = rows - 1
        keys = "[Enter] run  [Tab] next  [Shift+Tab/F3] prev  [F1] hint  [F2] reveal  [Ctrl+U] reset  [PgUp/PgDn] scroll  [Esc] quit"
        safe_addstr(self.stdscr, help_row, 0, truncate(keys, cols), curses.A_REVERSE)

        cur_screen_x = len(prompt) + (editor_cursor - scroll_x)
        try:
            self.stdscr.move(editor_row + 1, cur_screen_x)
        except curses.error:
            pass
        self.stdscr.refresh()
