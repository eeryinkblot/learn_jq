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
