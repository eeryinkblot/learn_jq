import pytest

from learn_jq.lessons import load_all
from learn_jq.validator import validate


def _all_lessons():
    return [(stage, lesson) for stage in load_all() for lesson in stage.lessons]


@pytest.mark.parametrize(
    "stage,lesson",
    _all_lessons(),
    ids=[f"stage{s.number}-{l.id}" for s, l in _all_lessons()],
)
def test_reference_filter_matches_expected(stage, lesson):
    result = validate(lesson.reference_filter, lesson.input_json, lesson.expected_outputs)
    assert result.passed, (
        f"Lesson {lesson.id} '{lesson.title}' reference_filter failed.\n"
        f"  filter:   {lesson.reference_filter}\n"
        f"  error:    {result.error}\n"
        f"  got:      {result.got_text}\n"
        f"  expected: {list(lesson.expected_outputs)}"
    )


def test_five_stages_present():
    stages = load_all()
    assert len(stages) == 5
    assert [s.number for s in stages] == [1, 2, 3, 4, 5]


def test_lesson_ids_unique():
    seen = set()
    for stage in load_all():
        for lesson in stage.lessons:
            assert lesson.id not in seen, f"duplicate lesson id: {lesson.id}"
            seen.add(lesson.id)


def test_every_stage_has_at_least_one_lesson():
    for stage in load_all():
        assert len(stage.lessons) > 0, f"stage {stage.number} has no lessons"
