from django.shortcuts import render
from rest_framework.views import APIView  
from rest_framework.generics import CreateAPIView
from django.http import JsonResponse  

import getpass
import os

from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader

from .serializers import UploadFileSerializer


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PATH_DOCS = os.environ.get('PATH_DOCS')

# Create your views here.
class HomeView(APIView):  

 def get(self, request, format=None):
    return JsonResponse({"message":
    'HOLA MUNDO DESDE DJANGO Y DOCKER', "content":
    'Por Mario Medina'}) 
 
class SumarizeView(CreateAPIView):  
   serializer_class = UploadFileSerializer

   def post(self, request, format=None):

      try:

         file_name = "doc_request.pdf"
         location = "{}/".format(os.environ.get("PATH_DOCS"))

         dataArchivo = request.FILES.copy()
         dataArchivo["location"] = location
         dataArchivo["file_name"] = file_name
         data = self.serializer_class(data=dataArchivo)

         if data.is_valid():
            file_name_save = data.save()  
            docs = PyPDFLoader(f"{location}{file_name_save}").load()

            os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY   

            llm = ChatOpenAI(model="gpt-4o-mini")
            prompt = ChatPromptTemplate.from_messages(
               [("system", "Escribe un resumen conciso de lo siguiente.:\\n\\n{context}")]
            )

            # Instantiate chain
            chain = create_stuff_documents_chain(llm, prompt)

            # Invoke chain
            result = chain.invoke({"context": docs})

            return JsonResponse({"message":
            '', "content":
            result})
         
      except Exception as e:
         print(e)
         return JsonResponse({"message":
         'Error al procesar la solicitud', "content":
         ''})