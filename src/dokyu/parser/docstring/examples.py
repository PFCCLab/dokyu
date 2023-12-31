# pyright: basic


from typing import Any

from parsita import Parser, ParserContext, lit, opt, reg, rep, success

from dokyu.parser.docstring.utils import double_indent, identifiers, indent
from dokyu.schema.docstring import Example


def to_example_code(example_code_lines: list[Any]) -> Parser[str, str]:
    return success("\n".join(example_code_lines))


def to_examples(examples_raw: list[Any]) -> Parser[str, list[Example]]:
    examples = []
    for example_info in examples_raw:
        lang_, label_, code = example_info
        lang = lang_.strip()
        label = label_.strip() if label_ else None
        examples.append(Example(description=None, lang=lang, label=label, code=code))
    return success(examples)


class ExamplesParser(ParserContext, whitespace=None):
    next_line = lit("\n") & indent
    blank_line = lit("\n")
    examples_head = lit("Examples:")
    example_code_block_head = indent >> reg(r".. code-block::\s*") >> identifiers << lit("\n")
    # example_code_block_description = rep(double_indent >> reg(r".*") << lit("\n"))
    example_code_block_label = opt(double_indent >> reg(r":name:\s*") >> reg(r".+") << lit("\n"))
    example_code_block_body = (
        rep((double_indent >> reg(r".+") << lit("\n")) | (lit("") << blank_line)) >= to_example_code
    )
    example_code_block = example_code_block_head & example_code_block_label << blank_line & example_code_block_body
    examples_body = lit("\n") >> rep(example_code_block << rep(blank_line))
    examples = examples_head >> examples_body >= to_examples
