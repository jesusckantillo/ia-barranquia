import sys
import os
from io import BytesIO
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))

from utils import __annotations__
from typing import Optional
from fastapi import File, APIRouter
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException 
from pydantic import BaseModel
from pathlib import Path
from services.ai_services.gemini_controller import  gemini_model
from services.audio_services.eleven_labs import sound_generator
from models.text.text_model import TextModel


router = APIRouter()

class TextCard(BaseModel):
    text1: str = ""
    text2: list[str] = []


@router.post("/get-mdx", response_class=FileResponse)
def generate_mdx(pdf_file: Optional[bytes] = File(description="File to send")):
    if not pdf_file:
        raise HTTPException(status_code=400, detail="Se requiere un archivo PDF")    
    mdx_file: 2
    return FileResponse(mdx_file, filename="generated.mdx")


@router.post("/get-audio/")
async def get_audio(word:str):
    sound_generator(word)  # Llamas a la función para generar el archivo
    file_path = "output.mp3"  # Ruta del archivo generado
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    Path(file_path).unlink()
    return FileResponse(BytesIO(audio_bytes), media_type="audio/mpeg")


@router.post("/text-card/")
def get_text_card(context: TextModel):
    word = context.word
    return gemini_model.generate_text_card(word)