from django.shortcuts import render
from app_semillitas.models import Evaluacion,Palabra,Usuario, Nivel
from django.db import Error,transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def addEvaluacion(request):
    try:
        usuario_id = request.POST['cbUsuarioId']
        idUsuario= Usuario.objects.get(pk=usuario)
        apellido
    except Error as e:
        return