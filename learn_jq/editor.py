class FilterEditor:
    def __init__(self) -> None:
        self._buf: list[str] = []
        self._cursor: int = 0

    @property
    def text(self) -> str:
        return "".join(self._buf)

    @property
    def cursor(self) -> int:
        return self._cursor

    def reset(self) -> None:
        self._buf = []
        self._cursor = 0

    def set_text(self, s: str) -> None:
        self._buf = list(s)
        self._cursor = len(self._buf)

    def insert(self, ch: str) -> None:
        self._buf.insert(self._cursor, ch)
        self._cursor += 1

    def backspace(self) -> None:
        if self._cursor > 0:
            del self._buf[self._cursor - 1]
            self._cursor -= 1

    def delete(self) -> None:
        if self._cursor < len(self._buf):
            del self._buf[self._cursor]

    def left(self) -> None:
        if self._cursor > 0:
            self._cursor -= 1

    def right(self) -> None:
        if self._cursor < len(self._buf):
            self._cursor += 1

    def home(self) -> None:
        self._cursor = 0

    def end(self) -> None:
        self._cursor = len(self._buf)
