from rest_framework import generics,status
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .views import *
import threading
from rest_framework_simplejwt.views import TokenObtainPairView

class AdminList(generics.ListCreateAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            admin= serializer.instance
            passwordGenerado = generar_password()
            admin.usuario_id.set_password(passwordGenerado)
            admin.usuario_id.save()

            asunto = "Registro de Usuario en el Sistema"
            mensajeCorreo = f"""
            Cordial Saludo <b>{admin.usuario_id.first_name} {admin.usuario_id.last_name}</b>, usted ha sido registrado
            en el sistema de Gestión Administradores de Semillitas Ampiu Sena.
            <br><br>nos permtimos enviar las credenciales de ingreso al sistema<br><br>
            <b>Username:</b> {admin.usuario_id.username}<br>
            <b>Password:</b> {passwordGenerado}<br>
            La URL del sistema es: https://127.0.0.1:8000/"""
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, [admin.usuario_id.email], None)
            )
            thread.start()
            return Response(
                {'mensaje':'Administrador creado correctamente','data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'mensaje':'Error al crear el Administrador','errores': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdminSerializer

class JugadorList(generics.ListCreateAPIView):
    queryset = Jugador.objects.all()
    serializer_class =JugadorSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            jugador= serializer.instance
            passwordGenerado = generar_password()
            jugador.usuario_id.set_password(passwordGenerado)
            jugador.usuario_id.save()

            asunto = "Registro de Jugador en el Sistema"
            mensajeCorreo = f"""
            Cordial Saludo <b>{jugador.usuario_id.first_name} {jugador.usuario_id.last_name}</b>, usted ha sido registrado
            en el sistema de Gestión Administradores de Semillitas Ampiu Sena.
            <br><br>nos permtimos enviar las credenciales de ingreso al sistema<br><br>
            <b>Username:</b> {jugador.usuario_id.username}<br>
            <b>Password:</b> {passwordGenerado}<br>
            La URL del sistema es: https://127.0.0.1:8000/"""
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, [jugador.usuario_id.email], None)
            )
            thread.start()
            return Response(
                {'mensaje':'Jugador creado correctamente','data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'mensaje':'Error al crear el Jugador','errores': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

class JugadorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer

class NivelList(generics.ListAPIView):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer
    permission_classes = [AllowAny] 

class EvaluacionList(generics.ListAPIView):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    permission_classes = [AllowAny] 

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer