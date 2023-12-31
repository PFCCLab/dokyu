from typing import Optional, Union

from pydantic import BaseModel


class Argument(BaseModel):
    name: str
    type: Optional[str]
    is_optional: bool
    description: str


class Return(BaseModel):
    type: Optional[str]
    description: str


class Example(BaseModel):
    lang: str
    description: Optional[str]
    label: Optional[str]
    code: str


class Warning(BaseModel):
    content: str


class Note(BaseModel):
    content: str


class Docstring(BaseModel):
    description: list[Union[str, Warning, Note]]
    args: list[Argument]
    returns: Optional[Return]
    examples: list[Example]
