from dataclasses import dataclass


@dataclass(frozen=True)
class Lesson:
    id: str
    title: str
    description: str
    input_json: str
    expected_outputs: tuple[str, ...]
    hint: str
    reference_filter: str


@dataclass(frozen=True)
class Stage:
    number: int
    name: str
    lessons: tuple[Lesson, ...]
