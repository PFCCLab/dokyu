# pyright: basic
from parsita import lit, opt, reg

indent = lit("    ")
double_indent = indent & indent
triple_indent = indent & double_indent
identifiers = reg(r"[a-zA-Z_][a-zA-Z0-9_]*")
whitespace = reg(r"\s+")
optional_whitespace = opt(whitespace)
