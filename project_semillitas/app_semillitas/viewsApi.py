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

class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdminSerializer

class JugadorList(generics.ListCreateAPIView):
    queryset = Jugador.objects.all()
    serializer_class =JugadorSerializer

class JugadorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer