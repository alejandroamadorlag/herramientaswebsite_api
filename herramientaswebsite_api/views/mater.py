from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from herramientaswebsite_api.serializers import *
from herramientaswebsite_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import string
import random
import json

#MATERIAS

class MateriasAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        materias = Materias.objects.order_by("nrc")
        lista = MateriasSerializer(materias, many=True).data
        
        return Response(lista, 200)

class Materiame(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        mater = request.mater
        #TODO: Regresar materia
        return Response({})

class MateriasView(generics.CreateAPIView):
 #Obtener materia por NRC
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        mater = get_object_or_404(Materias, nrc = request.GET.get("nrc"))
        mater = MateriasSerializer(mater, many=False).data

        return Response(mater, 200)
    
    #Registrar nueva materia
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        mater = MateriasSerializer(data=request.data)
        if mater.is_valid():
            #Create a profile for the materia
            materia = Materias.objects.create(nrc= request.data["nrc"],
                                              materia= request.data["materia"],
                                              seccion= request.data["seccion"],
                                              dias= request.data["dias"],
                                              hora_inicio= request.data["hora_inicio"],
                                              hora_final= request.data["hora_final"],
                                              salon= request.data["salon"],
                                              programa= request.data["programa"])
            materia.save()

            return Response({"materia_created_nrc": materia.nrc }, 201)

        return Response(materia.errors, status=status.HTTP_400_BAD_REQUEST)

#Para editar
class MateriaViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self, request, *args, **kwargs):
        mater = get_object_or_404(Materias, nrc=request.data["nrc"])
        mater.materia = request.data["materia"]
        mater.seccion = request.data["seccion"]
        mater.dias = request.data["dias"]
        mater.hora_inicio = request.data["hora_inicio"]
        mater.hora_final = request.data["hora_final"]
        mater.salon = request.data["salon"]
        mater.programa = request.data["programa"]
        mater.save()
        materia = MateriasSerializer(mater, many=False).data

        return Response(materia,200)
    
    def delete(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, nrc=request.GET.get("nrc"))
        try:
            materia.delete()
            return Response({"details":"Materia eliminada"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)