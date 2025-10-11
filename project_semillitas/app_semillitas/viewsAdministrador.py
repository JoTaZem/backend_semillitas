from django.shortcuts import render
from app_semillitas.models import Evaluacion,Palabra,Usuario, Nivel
from django.db import Error,transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from app_semillitas.views import enviarCorreo,generar_password
import threading

formato_fecha="%Y-%m-%d %H:%M:%S"

@csrf_exempt
def addEvaluacion(request):
    try:
        usuarioId = request.POST['cbUsuarioId']
        usuario = Usuario.objects.get(pk=usuarioId)
        nivelId = request.POST['cbNivelId']
        nivel =  Nivel.objects.get(pk=nivelId)
        fechaCreacion = request.POST['txtFechaCreacion']
        fecha_creada=datetime.strptime(fechaCreacion,formato_fecha)
        puntajeTotal = request.POST['txtPuntaje']

        evaluacion=Evaluacion(
            usuario_id=usuario,
            nivel_id= nivel,
            fecha = fecha_creada,
            puntaje=puntajeTotal
        )
        evaluacion.save()
        mensaje = "Evaluacion registrada correctamente"
    except Error as e:
        mensaje = "Error al registrar la Evaluacion: "+str(e)
    retorno={"mensaje":mensaje}
    return JsonResponse(retorno)

@csrf_exempt
def addPalabra(request):
    try:
        palEspan = request.POST['txtPalabraEspan']
        palAmpiu =  request.POST['txtPalabraAmpiu']
        nivelId = request.POST['cbNivelId']
        nivel =  Nivel.objects.get(pk=nivelId)
        palabra=Palabra(
            pal_español=palEspan,
            pal_ampiu=palAmpiu,
            nivel_id= nivel
        )
        palabra.save()
        mensaje = "Palabra registrada correctamente"
    except Error as e:
        mensaje = "Error al registrar la palabra: "+str(e)
    retorno={"mensaje":mensaje}
    return JsonResponse(retorno)

@csrf_exempt
def addAdmin(request):
    try:
        if(request.method=="POST"):
            nombres = request.POST['txtNombres'],
            apellidos = request.POST['txtApellidos'],
            correo = request.POST['txtCorreo'],
            fechaNacimiento = request.POST['txtFechaNacimieno'],
            with transaction.Atomic():
                usuario=Usuario(
                    first_name = nombres,
                    last_name = apellidos,
                    email = correo,
                    rol = "Admin",
                    username = correo
                )
                usuario.save()
                usuario.is_active = True
                passwordGenerado = generar_password()
                usuario.set_password(passwordGenerado)
                usuario.save()

                asunto = "Registro de Usuario en el Sistema"
                mensajeCorreo = f"""
                Cordial Saludo <b>{nombres} {apellidos}</b>, usted ha sido registrado
                en el sistema de Gestión Administradores de Semillitas Ampiu Sena.
                <br><br>nos permtimos enviar las credenciales de ingreso al sistema<br><br>
                <b>Username:</b> {correo}<br>
                <b>Password:</b> {passwordGenerado}<br>
                La URL del sistema es: https://127.0.0.1:8000/
                """
                thread = threading.Thread(
                    target=enviarCorreo, args=(asunto, mensajeCorreo, [correo], None)
                )
                thread.start()
            mensaje = "Administrador agregado correctamente..."
        else:
            mensaje = "No permitido"
    except Exception as e:
        transaction.rollback
        mensaje = e
    retorno = {"mensaje":mensaje,"username":correo,"password":passwordGenerado}    
    return JsonResponse(retorno)