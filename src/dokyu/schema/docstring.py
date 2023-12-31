from typing import Optional

from pydantic import BaseModel


class Argument(BaseModel):
    name: str
    type: Optional[str]
    is_optional: bool
    description: str
