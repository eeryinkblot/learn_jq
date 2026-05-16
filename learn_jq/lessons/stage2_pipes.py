from ..models import Lesson, Stage


STAGE = Stage(
    number=2,
    name="Pipes & Slices",
    lessons=(
        Lesson(
            id="2.1",
            title="The pipe operator",
            description=(
                "`a | b` feeds the output of `a` as the input to `b`. This is how "
                "you build filters step by step. Get the name of the first user."
            ),
            input_json='{"users": [{"name": "ada"}, {"name": "grace"}]}',
            expected_outputs=('"ada"',),
            hint="`.users | .[0] | .name`",
            reference_filter=".users | .[0] | .name",
        ),
        Lesson(
            id="2.2",
            title="Array slicing",
            description=(
                "`.[start:end]` returns a sub-array, like Python slicing. End is "
                "exclusive. Omit either side to slice from the start or to the end. "
                "Return the second and third elements."
            ),
            input_json='[10, 20, 30, 40, 50]',
            expected_outputs=("[20,30]",),
            hint="`.[1:3]`",
            reference_filter=".[1:3]",
        ),
        Lesson(
            id="2.3",
            title="Iterate with .[]",
            description=(
                "`.[]` emits each element of an array as a SEPARATE output value. "
                "Unlike `.`, it produces a stream of values, not a single array. "
                "Emit each user's name as its own output."
            ),
            input_json='[{"name": "ada"}, {"name": "grace"}, {"name": "linus"}]',
            expected_outputs=('"ada"', '"grace"', '"linus"'),
            hint="`.[] | .name`",
            reference_filter=".[] | .name",
        ),
        Lesson(
            id="2.4",
            title="Comma operator",
            description=(
                "`a, b` runs both filters on the same input and emits both results "
                "as separate values. Emit the name and the age as two outputs."
            ),
            input_json='{"name": "ada", "age": 36, "city": "London"}',
            expected_outputs=('"ada"', "36"),
            hint="`.name, .age`",
            reference_filter=".name, .age",
        ),
    ),
)
