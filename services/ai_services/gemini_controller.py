from pydantic import BaseModel
from typing import List
import google.generativeai as genai
import os
from dotenv import load_dotenv

class TextCard(BaseModel):
    translations: str = ""
    examples: List[str] = []


class GeminiModel:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.gemini_model = genai.GenerativeModel("gemini-pro")
    
    def generate_prompt(self, word):
        return f"Traducción de la palabra {word} al español y pequeños ejemplos de su uso en inglés. Dame la respuesta sin títulos (Ejemplos, palabra), ni signos especiales, solo texto. En la primera línea la traducción, y en las siguientes sus ejemplos: {word}"
    
    def generate_text_card(self, word):
        prompt = self.generate_prompt(word)
        response = self.gemini_model.generate_content(prompt)
        lista = response.text.splitlines()
        lista_filtrada = list(filter(None, lista))
        
        # Crear una instancia de TextCard
        card = TextCard(
            translations=lista_filtrada[0],  # La traducción debe estar en una lista
            examples=lista_filtrada[1:]
        )
        
        return card

load_dotenv()

API_KEY = os.getenv("API_KEY")
gemini_model = GeminiModel(api_key=API_KEY)
word = "hello"
text_card = gemini_model.generate_text_card(word)
print(text_card)
