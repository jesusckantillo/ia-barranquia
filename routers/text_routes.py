import sys
import os
import time
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))
import asyncio
from utils import __annotations__
from typing import Optional
from fastapi import File, APIRouter
from fastapi.responses import FileResponse, StreamingResponse
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


@router.get("/get-audio/")
async def get_audio(word: str):
    try:
        # Llama a la función para generar el archivo y obtiene la ruta del archivo
        file_path = sound_generator(word)
        
        # Espera hasta que el archivo esté completamente guardado (espera un máximo de 5 segundos)
        max_wait_time = 5  # segundos
        wait_interval = 0.1  # segundos
        waited_time = 0
        while not os.path.exists(file_path) and waited_time < max_wait_time:
            time.sleep(wait_interval)
            waited_time += wait_interval
        
        # Verifica si el archivo existe después de la espera
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        return file_path
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/text-card/")
def get_text_card(context: TextModel):
    word = context.word
    return gemini_model.generate_text_card(word)