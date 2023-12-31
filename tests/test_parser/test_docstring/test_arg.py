# pyright: basic

import pytest
from parsita import Success

from dokyu.parser.docstring.arg import ArgsParser
from dokyu.schema.docstring import Argument


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
    assert isinstance(ArgsParser.arg_type.parse(arg_type_string), Success)


@pytest.mark.parametrize(
    ("args_string", "expected"),
    [
        (
            """\
Args:
    arg_1 (int): Arg 1 is an integer.
    arg_2 (list[int|tuple[int, ...]] | tuple[int, ...]): Arg 2 is a list of integers.
""",
            [
                Argument(name="arg_1", type="int", is_optional=False, description="Arg 1 is an integer."),
                Argument(
                    name="arg_2",
                    type="list[int|tuple[int, ...]] | tuple[int, ...]",
                    is_optional=False,
                    description="Arg 2 is a list of integers.",
                ),
            ],
        ),
        (
            """\
Args:

    arg_1 (int): Arg 1 is an integer.
""",
            [
                Argument(name="arg_1", type="int", is_optional=False, description="Arg 1 is an integer."),
            ],
        ),
        (
            """\
Args:
    arg_1 (np.ndarray[int] | int): Arg 1 is an integer. This line is too long and will be wrapped
        with next line.
        and next line.
""",
            [
                Argument(
                    name="arg_1",
                    type="np.ndarray[int] | int",
                    is_optional=False,
                    description="Arg 1 is an integer. This line is too long and will be wrapped with next line. and next line.",
                ),
            ],
        ),
        (
            """\
Args:
    arg_1 (np.ndarray[int] | int): Arg 1 is an integer. This line is too long and will be wrapped
        with next line.
        and next line.
    arg_2 (np.ndarray[int] | int): Arg 1 is an integer. This line is too long and will be wrapped
        with next line.
        and next line.
""",
            [
                Argument(
                    name="arg_1",
                    type="np.ndarray[int] | int",
                    is_optional=False,
                    description="Arg 1 is an integer. This line is too long and will be wrapped with next line. and next line.",
                ),
                Argument(
                    name="arg_2",
                    type="np.ndarray[int] | int",
                    is_optional=False,
                    description="Arg 1 is an integer. This line is too long and will be wrapped with next line. and next line.",
                ),
            ],
        ),
        (
            """\
Parameters:
    arg_1 (int, optional): Arg 1 is an integer.
""",
            [
                Argument(name="arg_1", type="int", is_optional=True, description="Arg 1 is an integer."),
            ],
        ),
    ],
)
def test_parse_args(args_string: str, expected: list[Argument]):
    args_string = args_string
    res = ArgsParser.args.parse(args_string)
    assert isinstance(res, Success)
    assert res.unwrap() == expected
