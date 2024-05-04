from pydantic import BaseModel
from typing import List

class TextCard(BaseModel):
    word: str
    translations: List[str] = []
    examples: List[str] = []