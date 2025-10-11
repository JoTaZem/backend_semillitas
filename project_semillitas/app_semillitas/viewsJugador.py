from django.shortcuts import render
from app_semillitas.models import Evaluacion,Palabra,Usuario, Nivel
from django.db import Error,transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from app_semillitas.views import enviarCorreo,generar_password
import threading

