from learn_jq.progress import InMemoryProgress, Progress


def test_fresh_progress_reports_nothing_passed():
    p = InMemoryProgress()
    assert p.is_passed("1.1") is False
    assert p.passed_count(["1.1", "1.2"]) == 0


def test_mark_passed_then_is_passed():
    p = InMemoryProgress()
    p.mark_passed("1.1")
    assert p.is_passed("1.1") is True
    assert p.is_passed("1.2") is False


def test_stage_complete_requires_all_ids():
    p = InMemoryProgress()
    ids = ["1.1", "1.2", "1.3"]
    assert p.stage_complete(1, ids) is False
    p.mark_passed("1.1")
    p.mark_passed("1.2")
    assert p.stage_complete(1, ids) is False
    p.mark_passed("1.3")
    assert p.stage_complete(1, ids) is True


def test_passed_count():
    p = InMemoryProgress()
    p.mark_passed("1.1")
    p.mark_passed("1.3")
    assert p.passed_count(["1.1", "1.2", "1.3"]) == 2


class _DictProgress:
    def __init__(self):
        self._passed = {}

    def is_passed(self, lesson_id):
        return self._passed.get(lesson_id, False)

    def mark_passed(self, lesson_id):
        self._passed[lesson_id] = True

    def stage_complete(self, stage_number, lesson_ids):
        return all(self._passed.get(lid) for lid in lesson_ids)

    def passed_count(self, lesson_ids):
        return sum(1 for lid in lesson_ids if self._passed.get(lid))


def test_alternate_impl_satisfies_protocol():
    p: Progress = _DictProgress()
    p.mark_passed("x")
    assert p.is_passed("x")
    assert p.passed_count(["x", "y"]) == 1
