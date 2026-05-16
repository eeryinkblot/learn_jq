import json
import os
from pathlib import Path
from typing import Protocol


class Progress(Protocol):
    def is_passed(self, lesson_id: str) -> bool: ...
    def mark_passed(self, lesson_id: str) -> None: ...
    def stage_complete(self, stage_number: int, lesson_ids: list[str]) -> bool: ...
    def passed_count(self, lesson_ids: list[str]) -> int: ...


class InMemoryProgress:
    def __init__(self) -> None:
        self._passed: set[str] = set()

    def is_passed(self, lesson_id: str) -> bool:
        return lesson_id in self._passed

    def mark_passed(self, lesson_id: str) -> None:
        self._passed.add(lesson_id)

    def stage_complete(self, stage_number: int, lesson_ids: list[str]) -> bool:
        return all(lid in self._passed for lid in lesson_ids)

    def passed_count(self, lesson_ids: list[str]) -> int:
        return sum(1 for lid in lesson_ids if lid in self._passed)


def default_progress_path() -> Path:
    xdg = os.environ.get("XDG_DATA_HOME")
    base = Path(xdg) if xdg else Path.home() / ".local" / "share"
    return base / "learn_jq" / "progress.json"


class JsonFileProgress:
    def __init__(self, path: Path | None = None) -> None:
        self._path = Path(path) if path is not None else default_progress_path()
        self._passed: set[str] = set()
        self._load()

    @property
    def path(self) -> Path:
        return self._path

    def _load(self) -> None:
        try:
            data = json.loads(self._path.read_text())
        except FileNotFoundError:
            return
        except (json.JSONDecodeError, OSError):
            return
        passed = data.get("passed") if isinstance(data, dict) else None
        if isinstance(passed, list):
            self._passed = {x for x in passed if isinstance(x, str)}

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(self._path.suffix + ".tmp")
        tmp.write_text(json.dumps({"passed": sorted(self._passed)}))
        tmp.replace(self._path)

    def is_passed(self, lesson_id: str) -> bool:
        return lesson_id in self._passed

    def mark_passed(self, lesson_id: str) -> None:
        if lesson_id in self._passed:
            return
        self._passed.add(lesson_id)
        self._save()

    def stage_complete(self, stage_number: int, lesson_ids: list[str]) -> bool:
        return all(lid in self._passed for lid in lesson_ids)

    def passed_count(self, lesson_ids: list[str]) -> int:
        return sum(1 for lid in lesson_ids if lid in self._passed)
