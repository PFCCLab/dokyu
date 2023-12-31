# pyright: basic

import pytest
from parsita import Success

from dokyu.parser.docstring.returns import ReturnsParser
from dokyu.schema.docstring import Return


@pytest.mark.parametrize(
    ("returns_string", "expected"),
    [
        (
            """\
Returns:
    int: Return value is an integer.
""",
            Return(type="int", description="Return value is an integer."),
        ),
        (
            """\
Returns:

    list[int]: Return value is list of int, with a long description,
        which spans multiple lines.
""",
            Return(
                type="list[int]",
                description="Return value is list of int, with a long description,\nwhich spans multiple lines.",
            ),
        ),
    ],
)
def test_parse_returns(returns_string: str, expected: Return):
    res = ReturnsParser.returns.parse(returns_string)
    assert isinstance(res, Success)
    assert res.unwrap() == expected
