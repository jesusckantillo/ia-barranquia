from utils import __annotations__
from typing import Optional
from fastapi import File, FileResponse, APIRouter, Response
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException 
from pydantic import BaseModel

#Models import


router = APIRouter()

class TextCard(BaseModel):
    text1: str = ""
    text2: str[list] = []


@router.post("/get-mdx", response_class=FileResponse)
def generate_mdx(pdf_file: Optional[bytes] = File(description="File to send")):
    if not pdf_file:
        raise HTTPException(status_code=400, detail="Se requiere un archivo PDF")
    
    mdx_file: 2
    return FileResponse(mdx_file, filename="generated.mdx")

@router.post("/process-word/")
def process_word(word: str):
    #Procces    
    audio_blob = b'\x00\x01\x02\x03'  
    texts = ["Texto 1", "Texto 2"]  
    text_card = TextCard(text1=texts[0], text2=texts[1])
    return Response(audio_file, media_type="application/octet-stream"), text_card
