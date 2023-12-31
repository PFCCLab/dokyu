# pyright: basic

import pytest
from parsita import Success

from dokyu.parser.docstring.examples import ExamplesParser
from dokyu.schema.docstring import Example


@pytest.mark.parametrize(
    ("examples_string", "expected"),
    [
        (
            """\
Examples:
    .. code-block:: python

        >>> import paddle

        >>> a = paddle.to_tensor(1)
        >>> b = paddle.to_tensor(2)
        >>> paddle.add(a, b)
        Tensor(shape=[], dtype=int64, place=CPUPlace, stop_gradient=True)
""",
            [
                Example(
                    description=None,
                    lang="python",
                    label=None,
                    code="""\
>>> import paddle

>>> a = paddle.to_tensor(1)
>>> b = paddle.to_tensor(2)
>>> paddle.add(a, b)
Tensor(shape=[], dtype=int64, place=CPUPlace, stop_gradient=True)""",
                )
            ],
        ),
    ],
)
def test_parse_returns(examples_string: str, expected: list[Example]):
    res = ExamplesParser.examples.parse(examples_string)
    assert isinstance(res, Success)
    assert res.unwrap() == expected
