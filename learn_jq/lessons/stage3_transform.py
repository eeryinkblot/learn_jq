from ..models import Lesson, Stage


STAGE = Stage(
    number=3,
    name="Transformation",
    lessons=(
        Lesson(
            id="3.1",
            title="Object construction",
            description=(
                "Build a new object with `{key: filter, ...}`. Use it to project "
                "the fields you need. Build `{name, city}` from the input (the "
                "shorthand `{name}` is the same as `{name: .name}`)."
            ),
            input_json='{"name": "ada", "age": 36, "city": "London", "secret": "x"}',
            expected_outputs=('{"name":"ada","city":"London"}',),
            hint="`{name, city}` or `{name: .name, city: .city}`",
            reference_filter="{name, city}",
        ),
        Lesson(
            id="3.2",
            title="Array construction",
            description=(
                "Wrap a stream of values in `[...]` to collect them into an array. "
                "Collect every user's name into a single array."
            ),
            input_json='{"users": [{"name": "ada"}, {"name": "grace"}, {"name": "linus"}]}',
            expected_outputs=('["ada","grace","linus"]',),
            hint="`[.users[].name]`",
            reference_filter="[.users[].name]",
        ),
        Lesson(
            id="3.3",
            title="map(f)",
            description=(
                "`map(f)` is shorthand for `[.[] | f]` — apply a filter to each "
                "element and collect into an array. Double every number."
            ),
            input_json="[1, 2, 3, 4]",
            expected_outputs=("[2,4,6,8]",),
            hint="`map(. * 2)`",
            reference_filter="map(. * 2)",
        ),
        Lesson(
            id="3.4",
            title="select(cond)",
            description=(
                "`select(cond)` passes its input through if `cond` is true, "
                "otherwise emits nothing. Combined with `.[]`, it filters a stream. "
                "Emit only the users whose `active` field is true."
            ),
            input_json='[{"name": "ada", "active": true}, {"name": "bob", "active": false}, {"name": "eve", "active": true}]',
            expected_outputs=(
                '{"active":true,"name":"ada"}',
                '{"active":true,"name":"eve"}',
            ),
            hint="`.[] | select(.active)`",
            reference_filter=".[] | select(.active)",
        ),
        Lesson(
            id="3.5",
            title="length, keys, has",
            description=(
                "Built-ins to introspect values: `length` gives the size of an "
                "array/string/object, `keys` returns sorted object keys, `has(k)` "
                "tests membership. Return the keys of the input object."
            ),
            input_json='{"b": 2, "a": 1, "c": 3}',
            expected_outputs=('["a","b","c"]',),
            hint="`keys`",
            reference_filter="keys",
        ),
    ),
)
