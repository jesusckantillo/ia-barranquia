from pydantic import BaseModel

from typing import List

class TextCard(BaseModel):
    audio: bytes
    translations: List[str] = []
    examples: List[str] = []