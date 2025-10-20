from rest_framework import generics,status
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .views import *
import threading
from rest_framework_simplejwt.views import TokenObtainPairView

#Get y Post para el admin
class AdminList(generics.ListCreateAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return Jugador.objects.select_related('usuario').all()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            admin= serializer.instance
            passwordGenerado = generar_password()
            admin.usuario.set_password(passwordGenerado)
            admin.usuario.save()

            asunto = "Registro de Usuario en el Sistema"
            mensajeCorreo = f"""
            Cordial Saludo <b>{admin.usuario.first_name} {admin.usuario.last_name}</b>, usted ha sido registrado
            en el sistema de Gestión Administradores de Semillitas Ampiu Sena.
            <br><br>nos permtimos enviar las credenciales de ingreso al sistema<br><br>
            <b>Username:</b> {admin.usuario.username}<br>
            <b>Password:</b> {passwordGenerado}<br>
            La URL del sistema es: https://127.0.0.1:8000/"""
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, [admin.email], None)
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
#Update y delete admin
class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdminSerializer

#Get y Post Jugador
class JugadorList(generics.ListCreateAPIView):
    queryset = Jugador.objects.all()
    serializer_class =JugadorSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return Jugador.objects.select_related('usuario').all()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            
            return Response(
                {'mensaje':'Jugador creado correctamente','data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'mensaje':'Error al crear el Jugador','errores': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

#Put y Delete Jugador
class JugadorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    

class NivelList(generics.ListAPIView):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer
    permission_classes = [AllowAny] 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'mensaje': 'Nivel creada correctamente.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )
class NivelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nivel.objects.all()
    serializer_class = NivelSerializer


class EvaluacionList(generics.ListCreateAPIView):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    permission_classes = [AllowAny] 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'mensaje': 'Evaluación creada correctamente.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )
class PalabraList(generics.ListCreateAPIView):
    queryset = Palabra.objects.all()
    serializer_class = PalabraSerializer
    permission_classes = [AllowAny] 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'mensaje': 'Palabra creada correctamente.', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    