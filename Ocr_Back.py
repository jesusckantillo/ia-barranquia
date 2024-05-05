# Descripción: Este script se encarga de convertir un archivo PDF a imágenes y luego extraer el texto de las imágenes.
from difflib import SequenceMatcher
import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from difflib import SequenceMatcher

class OcrBack:
    def __init__(self, poppler_path, pdf_path, folder_path, output_mdx_path):
        self.poppler_path = poppler_path
        self.pdf_path = pdf_path
        self.folder_path = folder_path
        self.output_mdx_path = output_mdx_path

    def convert_pdf_to_images(self):
        """
        Converts a PDF file to a series of images.

        This method uses the pytesseract library to convert each page of the PDF file
        into an image and saves it as a JPEG file.

        Args:
            self (object): The instance of the class.

        Returns:
            None
        """
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pages = convert_from_path(pdf_path=self.pdf_path, poppler_path=self.poppler_path)
        saving_path = self.folder_path
        for i, page in enumerate(pages):
            page.save(os.path.join(saving_path, f"{os.path.splitext(os.path.basename(self.pdf_path))[0]}_page_{i}.jpg"), "JPEG")
            print(f"Image saved in {saving_path}")
        print("Process finished")

    def clean_text(self,text):
        # Remove unnecessary characters
        cleaned_text = text.replace('*', '')
        #quita todo simbolo especial, ejemplo: @#$%^&*()_+{}:"<>|\/
        cleaned_text = ''.join(e for e in cleaned_text if e.isalnum() or e.isspace())
        #agrega a la primera linea de texto el indicador de que es un titulo en markdown
        cleaned_text = "# " + cleaned_text
        # Remove extra spaces

        return cleaned_text

    def replace_mdx_content(self,file_path, new_content):
        with open(file_path, 'w') as file:
            cleaned_text = self.clean_text(new_content)
            file.write(cleaned_text)

    def extract_text_from_images(self):
        files = os.listdir(self.folder_path)
        textos_transcritos = {}
        for file in files:
            image_path = os.path.join(self.folder_path, file)
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            textos_transcritos[image_path] = text
        return textos_transcritos

    def save_text_to_mdx_files(self, textos_transcritos):
        for image_path, text in textos_transcritos.items():
            file_name = os.path.splitext(os.path.basename(image_path))[0] + ".mdx"
            file_path = os.path.join(self.output_mdx_path, file_name)
            with open(file_path, "w") as file:
                file.write(text)
            print(f"Transcribed text saved in {file_path}")

    @staticmethod
    def similarity(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def compare_text_similarity(self, text, text_to_compare):
        return self.similarity(text, text_to_compare)

# Example usage
if __name__ == "__main__":
    poppler_path = r"C:\Users\flavi\OneDrive\Escritorio\Proyectos personales\IA\Barranqui-ia\poppler-0.68.0\bin"
    pdf_path = r"C:\Users\flavi\OneDrive\Escritorio\Proyectos personales\IA\Barranqui-ia\Pdf_to_convert\archivo_prueba.pdf"
    folder_path = r"C:\Users\flavi\OneDrive\Escritorio\Proyectos personales\IA\Barranqui-ia\output_images"
    output_mdx_path = r"C:\Users\flavi\OneDrive\Escritorio\Proyectos personales\IA\Barranqui-ia\output_mdx"

    ocr = OcrBack(poppler_path, pdf_path, folder_path, output_mdx_path)
    ocr.convert_pdf_to_images()
    textos_transcritos = ocr.extract_text_from_images()
    for image_path, text in textos_transcritos.items():
        similarity_percentage = ocr.compare_text_similarity(text, textos_transcritos[image_path])
        print(f"{similarity_percentage}% similarity")
    ocr.save_text_to_mdx_files(textos_transcritos)


############################################################################################

