from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  
from .models import *

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        depth = 2
        extra_kwargs = {
            'password' :{'write_only': True},
        } 
    def create(self,validated_data):
        user =  Usuario(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class AdminSerializer(serializers.ModelSerializer):
    usuario_id=UsuariosSerializer()
    class Meta: 
        model = Administrador
        fields = '__all__'
    def create(self,validated_data):
        usuario_data = validated_data.pop('usuario_id')
        usuario = UsuariosSerializer().create(usuario_data) 
        admin = Administrador.objects.create(usuario_id=usuario,**validated_data)
        return admin
    
class JugadorSerializer(serializers.ModelSerializer):
    usuario_id=UsuariosSerializer()
    class Meta: 
        model = Jugador
        fields = '__all__'
    def create(self,validated_data):
        usuario_data = validated_data.pop('usuario_id')
        usuario = UsuariosSerializer().create(usuario_data) 
        jugador = Jugador.objects.create(usuario_id=usuario,**validated_data)
        return jugador
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user:Usuario):
        token = super().get_token(user)
        token['username'] = user.username
        token['rol'] = user.rol
        token['id'] = user.id
        token['nombre'] =  user.first_name
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.rol=='Admin':
            admin=Administrador.objects.filter(usuario_id=self.user).first()
            objetoRol = {
                "id" : admin.id,
            }
        else:
            jugador=Jugador.objects.filter(usuario_id=self.user).first()
            objetoRol = {
                "id" : jugador.id
            }
        data['user'] = {
            'id':self.user.id,
            'username':self.user.username,
            'rol':self.user.rol,

        }    
        return data 