from pydantic import BaseModel
from typing import List
import google.generativeai as genai
import os
from dotenv import load_dotenv
from Ocr_Back import OcrBack




class TextCard(BaseModel):
    translations: str = ""
    examples: List[str] = []

class PdfCard(BaseModel):
    text: str = ""

prompt_correct="""Procesar el texto de un archivo MDX extraído mediante OCR para eliminar imperfecciones y corregir errores gramaticales
Entrada:
texto ocr: texto extraído del archivo MDX mediante OCR.
Salida:
texto depurado:  texto depurado y corregido.
Pasos:
-Identificar imperfecciones.
-Caracteres especiales: Elimina caracteres no deseados como saltos de línea innecesarios, tabulaciones, etc.
-Errores de OCR: Busca patrones comunes de errores de OCR, como confusiones entre letras similares (e.j., "cl" por "d") o caracteres mal interpretados.
Espacios en blanco: Elimina espacios en blanco adicionales o incorrectos.
-Corrección gramatical:
    Divide el texto en oraciones.
    analiza cada oración y sugiere correcciones gramaticales.
    identifica y corrige errores ortográficos.
	Reemplaza las palabras mal escritas con las sugerencias de Gemini.
	Combina las oraciones corregidas nuevamente en un solo texto.
-Formato MDX:
 	Devuelve el "texto depurado" sin anotaciones (solo y únicamente el texto depurado) y manteniendo la estructura de un mdx"""
class GeminiModel:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.gemini_model = genai.GenerativeModel("gemini-pro")
    
    def generate_prompt_for_card(self, word):
        return f"Traducción de la palabra {word} al español y pequeños ejemplos de su uso en inglés. Dame la respuesta sin títulos (Ejemplos, palabra), ni signos especiales, solo texto. En la primera línea la traducción, y en las siguientes sus ejemplos: {word}"
    
    def generate_prompt_for_correct(self, text):
        return f"Procesar el texto de un archivo MDX extraído mediante OCR para eliminar imperfecciones y corregir errores gramaticales. Entrada: texto ocr: texto extraído del archivo MDX mediante OCR. Salida: texto depurado: texto depurado y corregido. Pasos: -Identificar imperfecciones. -Caracteres especiales: Elimina caracteres no deseados como saltos de línea innecesarios, tabulaciones, etc. -Errores de OCR: Busca patrones comunes de errores de OCR, como confusiones entre letras similares (e.j., 'cl' por 'd') o caracteres mal interpretados. Espacios en blanco: Elimina espacios en blanco adicionales o incorrectos. -Corrección gramatical: Divide el texto en oraciones. analiza cada oración y sugiere correcciones gramaticales. identifica y corrige errores ortográficos. Reemplaza las palabras mal escritas con las sugerencias de Gemini. Combina las oraciones corregidas nuevamente en un solo texto. -Formato MDX: Devuelve el 'texto depurado' sin anotaciones (solo y únicamente el texto depurado) y manteniendo la estructura de un mdx: {text}"
        
    def generate_pdf_card(self, text):
        prompt = self.generate_prompt_for_correct(text)
        response = self.gemini_model.generate_content(prompt)
        card = PdfCard(
            text=response.text
        )
        return card.text
    

    def generate_text_card(self, word):
        prompt = self.generate_prompt_for_card(word)
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
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCCj25CqkO5vOSVlhu26koEEEUQNpIZtcc'
API_KEY = os.getenv('GOOGLE_API_KEY')
gemini_model = GeminiModel(api_key=API_KEY)
""" word = "get up"
text_card = gemini_model.generate_text_card(word)
print(text_card) """

poppler_path = r"C:\Users\flavi\OneDrive\Escritorio\Proyectos personales\IA\Barranqui-ia\poppler-0.68.0\bin"
#pdf_path = r"C:\Users\flavi\OneDrive\Escritorio\Proyectos personales\IA\Barranqui-ia\Pdf_to_convert\archivo_prueba.pdf"
pdf_path = r"C:\Users\flavi\OneDrive\Escritorio\Proyectos personales\IA\Barranqui-ia\Pdf_to_convert\CV JesusCantillo.pdf"
folder_path = r"C:\Users\flavi\OneDrive\Escritorio\Proyectos personales\IA\Barranqui-ia\output_images"
output_mdx_path = r"C:\Users\flavi\OneDrive\Escritorio\Proyectos personales\IA\Barranqui-ia\output_mdx"


ocr = OcrBack(poppler_path=poppler_path, pdf_path=pdf_path, folder_path=folder_path, output_mdx_path=output_mdx_path)
ocr.convert_pdf_to_images()
textos_transcritos = ocr.extract_text_from_images()
ocr.save_text_to_mdx_files(textos_transcritos)

mdx_files = os.listdir(output_mdx_path)
for mdx_file in mdx_files:
    mdx_file_path = os.path.join(output_mdx_path, mdx_file)
    with open(mdx_file_path, 'r') as file:
        mdx_content = file.read()
        corrected_content = gemini_model.generate_pdf_card(mdx_content)
        ocr.replace_mdx_content(mdx_file_path, corrected_content)
    

""" for image_path, text in textos_transcritos.items():
    similarity_percentage = ocr.compare_text_similarity(text, pop)
    print(f"{similarity_percentage}% similarity")

 """
















pop="""
Valoración 1.5/5. El número, en miles, de toneladas de café que se venden diariamente en Colombia,  es 
una variable aleatoria continua con función de densidad dada por:  
𝑓(𝑥)={𝑐𝑥2, 𝑝𝑎𝑟𝑎 0≤𝑥 ≤3
0           𝑒𝑛 𝑜𝑡𝑟𝑜 𝑐𝑎𝑠𝑜   Si el costo de producir una tonelada es de $5’200.000 (pesos colombianos) COP y se vende a $2,092.32 
USD (Valor del dólar hoy: $3,058.80 COP): a. Encuentre el valor de la constante para el cual 𝑓(𝑥) es una función válida de densidad. b. ¿Cuál es la probabilidad de que en un día se obtenga una rentabilidad de más de un millón de dólares? 
(Tenga en cuenta que Rentabilidad=Ventas – Costos de producción) c. ¿Cuál es la rentabilidad diaria esperada?  d. El 60% de los días se venden más de cuántas toneladas?   2. Valoración 1.5/5 Una empresa produce láminas de acero. Se tienen dos procesos disponibles. Ambos 
producen láminas cuya longitud se distribuye normalmente. El proceso A tiene media de 4.1 m y 
desviación de 0.25 m, mientras que el proceso B, tiene media de 3.8 m. Además, se sabe que el 0.34% de 
las láminas del proceso B superan una longitud de 4.2065 m. Una lámina se considera defectuosa si su 
longitud es inferior a 3.45 m.  
a. Si se desea minimizar la proporción de láminas defectuosas, 
i. ¿cuál proceso prefiere?  
ii. Si ambos proceso tuvieran la misma media, ¿cuál proceso preferiría? Para los puntos b y c, asuma que todas las láminas provienen del proceso que usted escogió en el punto a (i). 
b. De un lote de 5000 láminas, ¿cuál es la probabilidad de que por lo menos 1000 de ellas no supere una 
longitud de 3.45 m?  Dé un resultado numérico, es decir, no deje la respuesta expresada. En caso de ser 
necesario, utilice alguna aproximación entre distribuciones.  
c. Para un trabajo particular se requieren dos láminas que midan por lo menos 3.6 m. La medición de cada 
lámina toma un tiempo de 15 segundos. ¿Cuál es la probabilidad de que nos demoremos más de 1 minuto 
en encontrar las dos láminas para el trabajo?   3. Valoración 2.0/5. Un molino de papel produce rollos de papel reciclado, por lo tanto se presentan 
pequeñas manchas (defectos observables) a lo largo de un rollo de papel. Si se conoce que en promedio 
se observan 5 defectos en 1 metro de papel y estos defectos ocurren aleatoriamente de acuerdo a un 
proceso de Poisson: a) Calcule la probabilidad de observar más de 100 defectos en un rollo de 40 metros Si se supone que la máquina de papel enrolla a una velocidad de 30 Mts/min y se cuenta con un dispositivo 
(infalible a esta velocidad) que detecta los defectos. b) ¿Cuál es la probabilidad de que transcurran máximo 5 segundos hasta que se detecte el próximo 
defecto?, ¿Qué se inclinaría a afirmar respecto a la tasa promedio de defectos, si a esa velocidad de 
máquina transcurren más de 5 segundos y no se detecta ningún defecto? c) (Asuma la misma velocidad de máquina). Ha transcurrido 1 segundo desde que se inició el dispositivo de 
detección y aún no se ha detectado ningún defecto. ¿Cuál es la probabilidad de que transcurran al menos 
4 segundos más hasta que ocurra una detección? Suponga ahora que la máquina corre a 500 mts/min y que el dispositivo de detección captura y reconoce 
imágenes a una tasa constante de 1000 cuadros por segundo (eso quiere decir que entre cada cuadro capturado 
hay un “tiempo ciego” 0.001 segundos entre cada cuadro). d) Calcule la probabilidad de que el dispositivo falle en la detección de defectos durante un “tiempo ciego
"""

text_tocorrect="""
1. Valoraci�dn 1.5/5. El numero, en miles, de toneladas de caf� que se venden diariamente en Colombia, es
una variable aleatoria continua con funcidn de densidad dada por:

f@) = ie para0<x <3
0 en otro caso

Si el costo de producir una tonelada es de $5�200.000 (pesos colombianos) COP y se vende a $2,092.32

USD (Valor del dolar hoy: $3,058.80 COP):

a. Encuentre el valor de la constante para el cual f(x) es una funci�n valida de densidad.

b. ~Cual es la probabilidad de que en un dia se obtenga una rentabilidad de mas de un mill�n de ddlares?
(Tenga en cuenta que Rentabilidad=Ventas � Costos de producci�n)

c. �Cual es la rentabilidad diaria esperada?

d. El60% de los dias se venden mas de cuantas toneladas?

2. \Valoraci�n 1.5/5 Una empresa produce laminas de acero. Se tienen dos procesos disponibles. Ambos
producen laminas cuya longitud se distribuye normalmente. El proceso A tiene media de 4.1 my
desviaci�n de 0.25 m, mientras que el proceso B, tiene media de 3.8 m. Ademas, se sabe que el 0.34% de
las laminas del proceso B superan una longitud de 4.2065 m. Una lamina se considera defectuosa si su
longitud es inferior a 3.45 m.

a. Sise desea minimizar la proporci�n de laminas defectuosas,

i. &cual proceso prefiere?
ii. Si ambos proceso tuvieran la misma media, {cual proceso preferiria?

Para los puntos b y c, asuma que todas las laminas provienen del proceso que usted escogi�d en el punto a (i).

b. Deun lote de 5000 laminas, �cual es la probabilidad de que por lo menos 1000 de ellas no supere una
longitud de 3.45 m? D� un resultado num�rico, es decir, no deje la respuesta expresada. En caso de ser
necesario, utilice alguna aproximaci6on entre distribuciones.

c. Para un trabajo particular se requieren dos laminas que midan por lo menos 3.6 m. La medici�n de cada
lamina toma un tiempo de 15 segundos. �Cual es la probabilidad de que nos demoremos mas de 1 minuto
en encontrar las dos laminas para el trabajo?

3. Valoraci�n 2.0/5. Un molino de papel produce rollos de papel reciclado, por lo tanto se presentan
pequefias manchas (defectos observables) a lo largo de un rollo de papel. Si se conoce que en promedio
se observan 5 defectos en 1 metro de papel y estos defectos ocurren aleatoriamente de acuerdo a un
proceso de Poisson:

a) Calcule la probabilidad de observar mas de 100 defectos en un rollo de 40 metros

Si se supone que la maquina de papel enrolla a una velocidad de 30 Mts/min y se cuenta con un dispositivo
(infalible a esta velocidad) que detecta los defectos.

b) ~Cual es la probabilidad de que transcurran maximo 5 segundos hasta que se detecte el pr�ximo
defecto?, � Qu� se inclinaria a afirmar respecto a la tasa promedio de defectos, si a esa velocidad de
maquina transcurren mas de 5 segundos y no se detecta ningun defecto?

c) (Asuma la misma velocidad de maquina). Ha transcurrido 1 segundo desde que se inici� el dispositivo de
detecci�n y aun no se ha detectado ningun defecto. �Cual es la probabilidad de que transcurran al menos
4 segundos mas hasta que ocurra una detecci6�n?

Suponga ahora que la maquina corre a 500 mts/min y que el dispositivo de detecci�n captura y reconoce
imagenes a una tasa constante de 1000 cuadros por segundo (eso quiere decir que entre cada cuadro capturado
hay un �tiempo ciego� 0.001 segundos entre cada cuadro).

d) Calcule la probabilidad de que el dispositivo falle en la detecci�n de defectos durante un �tiempo ciego�.

"""


new_pop2 = """
**Texto depurado:**

1. **Valoración:** 1.5/5. El número, en miles, de toneladas de café que se venden diariamente en Colombia, es una variable aleatoria continua con función de densidad dada por:

f(x) = 1/e para 0 < x < 3
0 en otro caso

Si el costo de producir una tonelada es de $5'200.000 (pesos colombianos) COP y se vende a $2,092.32 USD (Valor del dólar hoy: $3,058.80 COP):

a. Encuentre el valor de la constante para el cual f(x) es una función válida de densidad.

b. ¿Cuál es la probabilidad de que en un día se obtenga una rentabilidad de más de un millón de dólares? (Tenga en cuenta que Rentabilidad = Ventas - Costos de producción)

c. ¿Cuál es la rentabilidad diaria esperada?

d. El 60% de los días se venden más de ¿cuántas toneladas?

2. **Valoración:** 1.5/5. Una empresa produce láminas de acero. Se tienen dos procesos disponibles. Ambos producen láminas cuya longitud se distribuye normalmente. El proceso A tiene media de 4.1 m y desviación de 0.25 m, mientras que el proceso B tiene media de 3.8 m. Además, se sabe que el 0.34% de las láminas del proceso B superan una longitud de 4.2065 m. Una lámina se considera defectuosa si su longitud es inferior a 3.45 m.

a. Si se desea minimizar la proporción de láminas defectuosas,

i. ¿cuál proceso prefiere?
ii. Si ambos procesos tuvieran la misma media, ¿cuál proceso preferiría?

Para los puntos b y c, asuma que todas las láminas provienen del proceso que usted escogió en el punto a (i).

b. De un lote de 5000 láminas, ¿cuál es la probabilidad de que por lo menos 1000 de ellas no supere una longitud de 3.45 m? Dé un resultado numérico, es decir, no deje la respuesta expresada. En caso de ser necesario, utilice alguna aproximación entre distribuciones.

c. Para un trabajo particular se requieren dos láminas que midan por lo menos 3.6 m. La medición de cada lámina toma un tiempo de 15 segundos. ¿Cuál es la probabilidad de que nos demoremos más de 1 minuto en encontrar las dos láminas para el trabajo?

3. **Valoración:** 2.0/5. Un molino de papel produce rollos de papel reciclado, por lo que se presentan pequeñas manchas (defectos observables) a lo largo de un rollo de papel. Si se conoce que en promedio se observan 5 defectos en 1 metro de papel y estos defectos ocurren aleatoriamente de acuerdo con un proceso de Poisson:

a) Calcule la probabilidad de observar más de 100 defectos en un rollo de 40 metros.

Si se supone que la máquina de papel enrolla a una velocidad de 30 m/min y se cuenta con un dispositivo (infalible a esta velocidad) que detecta los defectos.

b) ¿Cuál es la probabilidad de que transcurran máximo 5 segundos hasta que se detecte el próximo defecto? ¿Qué se inclinaría a afirmar respecto a la tasa promedio de defectos, si a esa velocidad de máquina transcurren más de 5 segundos y no se detecta ningún defecto?

c) (Asuma la misma velocidad de máquina). Ha transcurrido 1 segundo desde que se inició el dispositivo de detección y aun no se ha detectado ningún defecto. ¿Cuál es la probabilidad de que transcurran al menos 4 segundos más hasta que ocurra una detección?

Suponga ahora que la máquina corre a 500 m/min y que el dispositivo de detección captura y reconoce imágenes a una tasa constante de 1000 cuadros por segundo (eso quiere decir que entre cada cuadro capturado hay un “tiempo ciego” de 0.001 segundos entre cada cuadro).

d) Calcule la probabilidad de que el dispositivo falle en la detección de defectos durante un “tiempo ciego”.
"""
# similarity_percentage = ocr.compare_text_similarity(pop, new_pop)
# print(f"{similarity_percentage}% similarity")


