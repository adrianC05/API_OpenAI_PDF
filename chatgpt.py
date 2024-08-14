# Importa las bibliotecas necesarias
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene la clave API de OpenAI desde la variable de entorno
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Inicializa el cliente de OpenAI con la clave API
client = OpenAI(api_key=OPENAI_API_KEY)

# Función para extraer texto de un archivo PDF usando PyPDF2
def extract_text_from_pdf_pypdf2(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Función para extraer citas bibliográficas (puedes mejorar la lógica de extracción)
def extract_citations_from_pdf(pdf_path):
    text = extract_text_from_pdf_pypdf2(pdf_path)
    # Implementar lógica para extraer citas específicamente si es necesario
    return text

# Especifica la ruta de los archivos PDF
pdf_path_1 = 'IA_articulo.pdf'
pdf_path_2 = 'IA_articulo_2.pdf'

# Extrae el texto de ambos PDFs
texto_pdf_1 = extract_text_from_pdf_pypdf2(pdf_path_1)
texto_pdf_2 = extract_text_from_pdf_pypdf2(pdf_path_2)

# Extrae las citas bibliográficas de ambos PDFs
citas_pdf_1 = extract_citations_from_pdf(pdf_path_1)
citas_pdf_2 = extract_citations_from_pdf(pdf_path_2)

# Define el prompt y el contexto para el análisis comparativo, incluyendo citas
prompt = (
    "Redacta una nueva introducción basada en las ideas presentadas en las introducciones de ambos documentos. "
    "Incorpora citas bibliográficas en formato APA en el texto. Las citas disponibles son las siguientes:\n\n"
    "Citas del Documento 1:\n" + citas_pdf_1 + "\n\n"
    "Citas del Documento 2:\n" + citas_pdf_2
)
contexto = "Eres un experto en análisis de documentos."

# Envía el texto a la API de OpenAI para su análisis
completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": contexto},
        {"role": "user", "content": f"{prompt}\n\nDocumento 1:\n{texto_pdf_1}\n\nDocumento 2:\n{texto_pdf_2}"}
    ]
)

# Imprime la respuesta del análisis
print(completion.choices[0].message.content)
