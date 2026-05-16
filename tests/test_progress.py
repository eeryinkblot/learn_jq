from learn_jq.progress import InMemoryProgress, JsonFileProgress, Progress


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


def test_json_file_progress_persists_across_instances(tmp_path):
    path = tmp_path / "nested" / "progress.json"
    p1 = JsonFileProgress(path)
    assert not p1.is_passed("1.1")
    p1.mark_passed("1.1")
    p1.mark_passed("2.3")
    assert path.exists()

    p2 = JsonFileProgress(path)
    assert p2.is_passed("1.1")
    assert p2.is_passed("2.3")
    assert not p2.is_passed("9.9")


def test_json_file_progress_missing_file_is_empty(tmp_path):
    p = JsonFileProgress(tmp_path / "does_not_exist.json")
    assert not p.is_passed("1.1")
    assert p.passed_count(["1.1", "1.2"]) == 0


def test_json_file_progress_corrupt_file_is_tolerated(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text("{ not valid json")
    p = JsonFileProgress(path)
    assert not p.is_passed("1.1")
    p.mark_passed("1.1")
    assert JsonFileProgress(path).is_passed("1.1")


def test_json_file_progress_unknown_shape_is_tolerated(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text('{"unrelated": 42}')
    p = JsonFileProgress(path)
    assert not p.is_passed("1.1")
