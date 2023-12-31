# pyright: basic
import pytest
from parsita import Success

from dokyu.parser.docstring.arg import ArgTypeParser


@pytest.mark.parametrize(
    "arg_type_string",
    [
        "int",
        "float",
        "str",
        "bool",
        "list",
        "tuple",
        "dict",
        "set",
        "Tensor",
        "paddle.Tensor",
        "np.ndarray[int]",
        "np.ndarray[np.int32]",
        "list[list[int]]",
        "list[int, int]",
        "tuple[int, ...] | list[int]",
        "list[int | tuple[str, ...]]",
    ],
)
def test_parse_arg_type(arg_type_string: str):
    assert isinstance(ArgTypeParser.arg_type.parse(arg_type_string), Success)
