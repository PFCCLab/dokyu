# pyright: basic
# pyright: reportUndefinedVariable=false

from parsita import ParserContext, lit, opt, rep

from dokyu.parser.docstring.utils import identifiers, optional_whitespace


class ArgTypeParser(ParserContext, whitespace=None):
    ellipsis = lit("...")
    type_generic = (
        identifiers
        & lit("[")
        & arg_type
        & rep(optional_whitespace & lit(",") & optional_whitespace & arg_type)
        & lit("]")
    )
    arg_type = (
        (identifiers | ellipsis | type_generic)
        & opt(optional_whitespace & lit("|") & optional_whitespace & arg_type)  # For union, no left recursion
        & opt(lit(".") & arg_type)  # For getattr, no left recursion
    )
