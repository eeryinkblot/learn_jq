from learn_jq.validator import validate


def test_field_access_passes():
    r = validate(".foo", '{"foo": 1}', ("1",))
    assert r.passed and r.error is None


def test_bracket_form_equivalent_to_field_access():
    r = validate('.["foo"]', '{"foo": 1}', ("1",))
    assert r.passed, f"got_text={r.got_text}, error={r.error}"


def test_key_order_insensitivity():
    r = validate(".", '{"a": 1, "b": 2}', ('{"b":2,"a":1}',))
    assert r.passed


def test_array_order_is_significant():
    r = validate("[2,1]", "null", ("[1,2]",))
    assert not r.passed


def test_multi_value_stream():
    r = validate(".[]", "[1,2,3]", ("1", "2", "3"))
    assert r.passed


def test_wrong_count_fails():
    r = validate(".[]", "[1,2]", ("1", "2", "3"))
    assert not r.passed


def test_syntax_error_returns_failure_not_exception():
    r = validate("bogus(", "null", ("null",))
    assert not r.passed
    assert r.error is not None


def test_missing_field_yields_null():
    r = validate(".missing", '{"foo":1}', ("null",))
    assert r.passed


def test_int_vs_float_treated_equal_when_one_side_float():
    r = validate("1", "null", ("1.0",))
    assert r.passed


def test_nested_object_compare():
    r = validate(
        '{a: 1, b: {c: 2, d: 3}}',
        "null",
        ('{"b":{"d":3,"c":2},"a":1}',),
    )
    assert r.passed
