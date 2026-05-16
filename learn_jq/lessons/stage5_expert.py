from ..models import Lesson, Stage


STAGE = Stage(
    number=5,
    name="Expert",
    lessons=(
        Lesson(
            id="5.1",
            title="Custom functions",
            description=(
                "Define functions with `def name: body;` and call them by name. "
                "Functions can take arguments too: `def add(x): . + x;`. "
                "Define `double` (multiplies its input by 2) and apply it to "
                "every element of the input array."
            ),
            input_json="[1, 2, 3, 4]",
            expected_outputs=("[2,4,6,8]",),
            hint="`def double: . * 2; map(double)`",
            reference_filter="def double: . * 2; map(double)",
        ),
        Lesson(
            id="5.2",
            title="Regex with capture",
            description=(
                "`test(re)` returns a boolean. `capture(re)` returns an object "
                "with named groups as fields. Capture the year and month from "
                "each date string in the array."
            ),
            input_json='["2024-01-15", "2025-11-03"]',
            expected_outputs=(
                '[{"month":"01","year":"2024"},{"month":"11","year":"2025"}]',
            ),
            hint=r'`map(capture("(?<year>\\d{4})-(?<month>\\d{2})"))`',
            reference_filter=r'map(capture("(?<year>\\d{4})-(?<month>\\d{2})") | {year, month})',
        ),
        Lesson(
            id="5.3",
            title="recurse and ..",
            description=(
                "`..` (recursive descent) walks every value in a structure — "
                "every object, array, scalar, leaf, all of it. Combine with "
                "`select` to find values anywhere. Find every `name` field "
                "anywhere in the input, as a stream of strings."
            ),
            input_json=(
                '{"name":"root","children":['
                '{"name":"a","children":[{"name":"a1"}]},'
                '{"name":"b"}'
                ']}'
            ),
            expected_outputs=('"root"', '"a"', '"a1"', '"b"'),
            hint="`.. | .name? // empty`",
            reference_filter=".. | .name? // empty",
        ),
        Lesson(
            id="5.4",
            title="Path expressions and del",
            description=(
                "`paths` emits every path in the structure as an array. "
                "`del(path)` removes a value at a path. `getpath`/`setpath` "
                "read/write at a path. Delete the `secret` field from every "
                "user."
            ),
            input_json=(
                '{"users":['
                '{"name":"ada","secret":"x"},'
                '{"name":"bob","secret":"y"}'
                ']}'
            ),
            expected_outputs=(
                '{"users":[{"name":"ada"},{"name":"bob"}]}',
            ),
            hint="`del(.users[].secret)`",
            reference_filter="del(.users[].secret)",
        ),
        Lesson(
            id="5.5",
            title="Streaming with tostream",
            description=(
                "`tostream` converts a value into a stream of [path, leaf] "
                "pairs (plus [path] end markers). This is the same shape jq "
                "emits in `--stream` mode and lets you process huge inputs "
                "without loading them whole. Convert the input to its stream "
                "form."
            ),
            input_json='{"a": 1, "b": [10, 20]}',
            expected_outputs=(
                '[["a"],1]',
                '[["b",0],10]',
                '[["b",1],20]',
                '[["b",1]]',
                '[["b"]]',
            ),
            hint="`tostream`",
            reference_filter="tostream",
        ),
    ),
)
