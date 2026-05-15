from ..models import Lesson, Stage


STAGE = Stage(
    number=1,
    name="Basics",
    lessons=(
        Lesson(
            id="1.1",
            title="Identity",
            description=(
                "The simplest jq filter is `.` (a single dot). It returns its input "
                "unchanged. This is your first building block: every other filter is "
                "composed from transformations of `.`."
            ),
            input_json='{"hello": "world"}',
            expected_outputs=('{"hello":"world"}',),
            hint="Just type a single period.",
            reference_filter=".",
        ),
        Lesson(
            id="1.2",
            title="Field access",
            description=(
                "Use `.fieldname` to extract a field from an object. The result is "
                "the value of that field."
            ),
            input_json='{"name": "ada", "age": 36}',
            expected_outputs=('"ada"',),
            hint="`.name`",
            reference_filter=".name",
        ),
        Lesson(
            id="1.3",
            title="Nested fields",
            description=(
                "Chain field accesses with more dots to reach into nested objects. "
                "Get the email from the user object."
            ),
            input_json='{"user": {"name": "ada", "email": "ada@example.com"}}',
            expected_outputs=('"ada@example.com"',),
            hint="`.user.email`",
            reference_filter=".user.email",
        ),
        Lesson(
            id="1.4",
            title="Array indexing",
            description=(
                "Arrays are indexed with `.[N]` where N can be negative to count "
                "from the end. Get the LAST element of the array."
            ),
            input_json='["apple", "banana", "cherry"]',
            expected_outputs=('"cherry"',),
            hint="`.[-1]` or `.[2]`",
            reference_filter=".[-1]",
        ),
        Lesson(
            id="1.5",
            title="Bracket form for odd keys",
            description=(
                "If a key has spaces, dashes, or special characters, `.foo-bar` "
                "won't work. Use `.[\"foo-bar\"]` instead. Get the value of the "
                "\"full name\" key."
            ),
            input_json='{"full name": "Ada Lovelace", "id": 1}',
            expected_outputs=('"Ada Lovelace"',),
            hint='`.["full name"]`',
            reference_filter='.["full name"]',
        ),
    ),
)
