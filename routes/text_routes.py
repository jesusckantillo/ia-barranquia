from utils import __annotations__
from typing import Optional
from fastapi import File, FileResponse, APIRouter
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException 
#Models import
from data.models.text.card_model import TextCard



router = APIRouter()


@router.post("/get_mdx", response_class=FileResponse)
def generate_mdx(pdf_file: Optional[bytes] = File(description="File to send")):
    if not pdf_file:
        raise HTTPException(status_code=400, detail="Se requiere un archivo PDF")
    
    mdx_file: 2
    return FileResponse(mdx_file, filename="generated.mdx")



@router.post("/get_card", response_class=TextCard)
def generate_card():
  pass

