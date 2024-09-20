from django.shortcuts import render
from rest_framework.views import APIView  
from rest_framework.generics import CreateAPIView
from django.http import JsonResponse  
from langchain_core.pydantic_v1 import BaseModel, Field

import os
import json

# from langchain.chains import create_structured_output_runnable
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, Docx2txtLoader
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from .serializers import UploadFilePDFSerializer, UploadFileWordSerializer

# Constantes
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PATH_DOCS = os.environ.get('PATH_DOCS')
VALID_EXTENSIONS = ["pdf", "docx", "doc"]
PROMPT_SYSTEM_TEMPLATE = '''Eres un asistente que solo habla en JSON. No genere salida que no esté en JSON correctamente formateada.
Se te va a proporcionar un documento en formato PDF o Word y debes retornar en formato JSON los siguientes campos:

- summarize: <str> Un resumen conciso del documento, omitiendo saludos y despedidas. Máximo 500 caracteres. 
- fecha_doc: <date> La fecha del documento en formato dd/mm/yyyy.
- tipo_doc: <str> El tipo de documento.
- number_doc: <str> El número del documento.
- year_doc: <str> El año del documento.
- siglas_doc: <str> Las siglas del documento.
- oficina_destino: <str> La oficina de destino del documento.


Ejemplo: Se te pasa el siguiente documento:

*******************************************************************************
“Año del Bicentenario, de la consolidación de nuestra Independencia, y de la conmemoración de las heroicas batallas de Junín y Ayacucho”


MEMORANDO Nº002-2024-OGTI/MPP

A		:     ING. JOHAN HUEBNER LADERA ESPINOZA
                                Jefe de la Oficina de Desarrollo de Tecnologías
 
ASUNTO       :	ACTUALIZACION DE REPORTE DE CUMPLIMIENTO DIGITAL

REF.               :	EXP. 07807-2023 PCM SECRETARIA DE GOBIERNO DIGITAL
	EXP. 010224-2023 PCM SECRETARIA DE GOBIERNO DIGITAL

FECHA          :	San Miguel de Piura, enero 11 de 2024.
	------------------------------------------------------------------------------------------
                              Por medio del presente, solicito a usted, se sirva efectuar la revisión y actualización de la documentación sustentante para la Actualización del Reporte de Cumplimiento Digital; según lo descrito en OFICIO NºD00624-2023-PCM-SGTD, presentado por Secretaría de Gobierno y Transformación Digital a través de los expedientes Nº07809 y 010224 del año 2023.
 
			Atentamente,
*******************************************************************************

Debes retornar lo siguiente en formato JSON:
{{
   "summarize": "Solicito a usted, se sirva efectuar la revisión y actualización de la documentación sustentante para la Actualización del Reporte de Cumplimiento Digital; según lo descrito en OFICIO NºD00624-2023-PCM-SGTD, presentado por Secretaría de Gobierno y Transformación Digital a través de los expedientes Nº07809 y 010224 del año 2023.",
   "fecha_doc": "11/01/2024",
   "tipo_doc": "MEMORANDO",
   "number_doc": "002",
   "year_doc": "2024",
   "siglas_doc": "OGTI/MPP"
   "oficina_destino": Oficina de Desarrollo de Tecnologías
}}



{context}'''

# Cargar dependencias desde el archivo JSON
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'dependencias.json')

with open(json_path, 'r', encoding='utf-8') as file:
    dependencias = json.load(file)

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Funciones auxiliares
def get_docs_from_pdf(file_name):
    return PyPDFLoader(file_name).load()

def get_docs_from_word(file_name):
    return Docx2txtLoader(file_name).load()

def get_file_extension(file_name):
    return file_name.split(".")[-1]

def is_valid_extension(extension):
    return extension in VALID_EXTENSIONS

def get_serializer_class(extension):
    if extension == "pdf":
        return UploadFilePDFSerializer
    return UploadFileWordSerializer

def summarize_docs(docs):    
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt = ChatPromptTemplate.from_messages(
        [("system", PROMPT_SYSTEM_TEMPLATE)]
    )
    parser = JsonOutputParser(pydantic_object=DocumentFormat)
    chain = create_stuff_documents_chain(llm, prompt, output_parser=parser)

    # Invoke chain
    return chain.invoke({"context": docs})    

class DocumentFormat(BaseModel):
    """Retorna los principales datos del documento"""

    summarize: str = Field(..., description="Un resumen conciso del documento omitiendo saludos y despedidas.")
    fecha_doc: str = Field(..., description="La fecha del documento ")
    tipo_doc: str = Field(..., description="El tipo de documento.")
    number_doc: str = Field(..., description="El número del documento.")
    year_doc: str = Field(..., description="El año del documento.")
    siglas_doc: str = Field(..., description="Las siglas del documento.")
    oficina_destino: str = Field(..., description="La oficina de destino del documento.")
    


# Vistas
class HomeView(APIView):  
    def get(self, request, format=None):
        return JsonResponse({"message": 'HOLA MUNDO DESDE DJANGO Y DOCKER', "content": 'Por Mario Medina'}) 

class SumarizeView(CreateAPIView):  
    def post(self, request, format=None):
        try:            
            file_name = "doc_request.pdf"
            location = f"{PATH_DOCS}/"

            dataArchivo = request.FILES.copy()
            dataArchivo["location"] = location
            dataArchivo["file_name"] = file_name

            request_file_name = dataArchivo["archivo"].name
            extension = get_file_extension(request_file_name)
            
            if not is_valid_extension(extension):
                return JsonResponse({"message": 'Tipo de archivo no permitido', "content": ''})

            self.serializer_class = get_serializer_class(extension)
            data = self.serializer_class(data=dataArchivo)

            if data.is_valid():
                file_name_save = data.save()
                file_path = f"{location}{file_name_save}"
                
                if extension == "pdf":
                    docs = get_docs_from_pdf(file_path)
                else:
                    docs = get_docs_from_word(file_path)

                result = summarize_docs(docs)

                name_office_destiny =  result.get("oficina_destino", "")
                # modificar el nombre de la oficina de destino quitando los acentos y poner en minusculas
                name_office_destiny_format = name_office_destiny.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").upper()

                print(dependencias.get(name_office_destiny_format, ""))

                result["cod_oficina_destino"] = dependencias.get(name_office_destiny_format, 0)
                print("************************* result *************************")
                print(result)
                # return JsonResponse({"message": '', "content": result})
                response = JsonResponse({"message": '', "content": result})
                response['Content-Type'] = 'application/json; charset=utf-8'
                return response
                
            
        except Exception as e:
            print(e)
            return JsonResponse({"message": str(e.args), "content": 'Error en el servidor'})