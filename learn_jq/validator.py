import json
import subprocess
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Result:
    passed: bool
    got_text: str = ""
    error: str | None = None


def _normalize(v: Any) -> Any:
    if isinstance(v, dict):
        return {k: _normalize(v[k]) for k in sorted(v.keys())}
    if isinstance(v, list):
        return [_normalize(x) for x in v]
    return v


def _values_equal(a: Any, b: Any) -> bool:
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            return False
        return all(_values_equal(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        return all(_values_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if isinstance(a, float) or isinstance(b, float):
            return float(a) == float(b)
        return a == b
    return a == b


def _parse_stream(text: str) -> list[Any]:
    out = []
    for line in text.split("\n"):
        if not line:
            continue
        out.append(json.loads(line))
    return out


def validate(
    filter_text: str,
    input_json: str,
    expected_outputs: tuple[str, ...] | list[str],
) -> Result:
    try:
        proc = subprocess.run(
            ["jq", "-c", filter_text],
            input=input_json,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        return Result(passed=False, error="timed out")
    except FileNotFoundError:
        return Result(passed=False, error="jq not found on PATH")

    if proc.returncode != 0:
        return Result(passed=False, got_text=proc.stdout, error=proc.stderr.strip())

    try:
        got = _parse_stream(proc.stdout)
    except json.JSONDecodeError as e:
        return Result(passed=False, got_text=proc.stdout, error=f"could not parse jq output: {e}")

    try:
        want = [json.loads(s) for s in expected_outputs]
    except json.JSONDecodeError as e:
        return Result(passed=False, got_text=proc.stdout, error=f"bad expected_outputs in lesson: {e}")

    got_n = [_normalize(v) for v in got]
    want_n = [_normalize(v) for v in want]

    passed = len(got_n) == len(want_n) and all(_values_equal(g, w) for g, w in zip(got_n, want_n))
    return Result(passed=passed, got_text=proc.stdout.strip())
