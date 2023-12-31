# pyright: basic
# pyright: reportUndefinedVariable=false

from typing import Any

from parsita import Parser, ParserContext, lit, opt, reg, rep, success

from dokyu.parser.docstring.utils import double_indent, identifiers, indent, optional_whitespace
from dokyu.schema.docstring import Return


def to_return(return_: list[Any]) -> Parser[str, Return]:
    type_, description_ = return_

    if type_:
        type = type_[0].strip()
        assert isinstance(type, str)
        if type.endswith("optional"):
            is_optional = True
            type = type[: type.rfind(",")].strip()
    else:
        type = None

    description_first_line = description_[0]
    description_rest_lines = description_[1]
    description = "\n".join([description_first_line] + description_rest_lines)
    res = success(Return(type=type, description=description))
    return res


def to_returns(returns: Return) -> Parser[str, Return]:
    return success(returns)


class ReturnsParser(ParserContext, whitespace=None):
    next_line = lit("\n") & indent
    blank_line = lit("\n")
    returns_head = lit("Returns:")
    return_type = reg(r"[^:,]+")
    return_doc = optional_whitespace >> reg(r".*") & rep("\n" >> double_indent >> reg(r".*"))
    return_ = opt(return_type << (lit(":") | lit(","))) & return_doc >= to_return
    returns_body = rep(lit("\n"), min=1) >> indent >> return_ << rep(blank_line)
    returns = returns_head >> returns_body >= to_returns
