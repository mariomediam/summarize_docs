from django.shortcuts import render
from rest_framework.views import APIView  
from django.http import JsonResponse  

# Create your views here.
class HomeView(APIView):  

 def get(self, request, format=None):
    return JsonResponse({"message":
    'HOLA MUNDO DESDE DJANGO Y DOCKER', "content":
    'Por Mario Medina'}) 