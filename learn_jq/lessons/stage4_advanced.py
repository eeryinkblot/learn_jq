from ..models import Lesson, Stage


STAGE = Stage(
    number=4,
    name="Advanced",
    lessons=(
        Lesson(
            id="4.1",
            title="group_by and sort_by",
            description=(
                "`group_by(f)` groups elements with the same `f` value into "
                "sub-arrays (also sorted by f). `sort_by(f)` sorts a stream. "
                "Group the users by their `dept`."
            ),
            input_json=(
                '[{"name":"ada","dept":"eng"},'
                '{"name":"bob","dept":"sales"},'
                '{"name":"eve","dept":"eng"}]'
            ),
            expected_outputs=(
                '[[{"dept":"eng","name":"ada"},{"dept":"eng","name":"eve"}],'
                '[{"dept":"sales","name":"bob"}]]',
            ),
            hint="`group_by(.dept)`",
            reference_filter="group_by(.dept)",
        ),
        Lesson(
            id="4.2",
            title="reduce",
            description=(
                "`reduce STREAM as $x (INIT; UPDATE)` folds a stream into a single "
                "value. `$x` is the current element; `.` inside UPDATE is the "
                "accumulator. Sum the numbers."
            ),
            input_json="[1, 2, 3, 4, 5]",
            expected_outputs=("15",),
            hint="`reduce .[] as $x (0; . + $x)`",
            reference_filter="reduce .[] as $x (0; . + $x)",
        ),
        Lesson(
            id="4.3",
            title="Variable binding with `as`",
            description=(
                "`EXPR as $name | BODY` binds the value of EXPR to `$name` for "
                "use inside BODY. Useful when you need a value from elsewhere in "
                "the structure. Return `{user: .name, company: $company}` where "
                "$company is bound from `.company.name`."
            ),
            input_json='{"name": "ada", "company": {"name": "AnalyticalEngines"}}',
            expected_outputs=('{"company":"AnalyticalEngines","user":"ada"}',),
            hint="`.company.name as $company | {user: .name, company: $company}`",
            reference_filter=".company.name as $company | {user: .name, company: $company}",
        ),
        Lesson(
            id="4.4",
            title="if / then / elif / else / end",
            description=(
                "Conditional expressions. The `end` keyword is required. Map "
                "each number to \"neg\", \"zero\", or \"pos\"."
            ),
            input_json="[-2, 0, 3, -1, 5]",
            expected_outputs=('["neg","zero","pos","neg","pos"]',),
            hint='`map(if . < 0 then "neg" elif . == 0 then "zero" else "pos" end)`',
            reference_filter='map(if . < 0 then "neg" elif . == 0 then "zero" else "pos" end)',
        ),
        Lesson(
            id="4.5",
            title="Update assignment |=",
            description=(
                "`PATH |= filter` updates each value at PATH by applying `filter` "
                "to it. Different from `PATH = expr`, which sets PATH to the "
                "value of `expr` (evaluated in the outer context). Increment "
                "every user's `age` by 1."
            ),
            input_json='{"users": [{"name":"ada","age":36},{"name":"bob","age":40}]}',
            expected_outputs=(
                '{"users":[{"age":37,"name":"ada"},{"age":41,"name":"bob"}]}',
            ),
            hint="`.users |= map(.age += 1)` or `.users[].age += 1`",
            reference_filter=".users |= map(.age += 1)",
        ),
    ),
)
