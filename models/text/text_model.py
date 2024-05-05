from pydantic import BaseModel

class TextModel(BaseModel):
    word: str
    context:str

class WordToAudio(BaseModel):
    word: str