# pyright: basic
# pyright: reportUndefinedVariable=false

from typing import Any

from parsita import Parser, ParserContext, lit, opt, reg, rep, success

from dokyu.parser.docstring.utils import double_indent, identifiers, indent, optional_whitespace
from dokyu.schema.docstring import Argument


def to_argument(arg: list[Any]) -> Parser[str, Argument]:
    name, type_, description_ = arg
    type = type_[0] if type_ else None
    description_first_line = description_[0]
    description_rest_lines = description_[1]
    description = " ".join([description_first_line] + description_rest_lines)
    return success(Argument(name=name, type=type, description=description))


def to_arguments(args: list[Any]) -> Parser[str, list[Argument]]:
    return success([arg for arg in args if isinstance(arg, Argument)])


class ArgsParser(ParserContext, whitespace=None):
    next_line = "\n" & indent
    blank_line = "\n"
    args_head = lit("Args:")
    arg_type = reg(r"[^)]+")
    arg_doc = optional_whitespace >> reg(r".*") & rep("\n" >> double_indent >> reg(r".*"))
    # TODO(SigureMo): Deal *args and **kwargs
    arg = (
        identifiers & optional_whitespace >> opt(lit("(") >> arg_type << lit(")")) & lit(":") >> arg_doc >= to_argument
    )
    args_body = rep(next_line >> arg | blank_line, min=1)
    args = args_head >> args_body >= to_arguments
