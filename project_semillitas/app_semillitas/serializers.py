from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  
from .models import *
from django.db import transaction


class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = '__all__'
class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = '__all__'
                
class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        depth = 2
        extra_kwargs = {
            'password' :{'write_only': True, 'required':False, 'allow_null':True},
        } 
    def create(self,validated_data):
        user =  Usuario(**validated_data)
        password = validated_data.get('password')
        if password and password.strip():
            user.set_password(password)
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
        read_only_fields = ('usuario_id',)
    @transaction.atomic    
    def create(self, validated_data):
        # 1. Crear el Usuario
        usuario_data = validated_data.pop('usuario_id')
        usuario = UsuariosSerializer().create(usuario_data) 
        
        # 2. 🔑 CLAVE: Limpiar los campos de Usuario que se filtraron
        #    Esto soluciona el "TypeError: 'username' is an invalid keyword argument..."
        usuario_fields_to_remove = ['username', 'email', 'first_name', 'last_name', 'rol', 'password']
        for field in usuario_fields_to_remove:
            # Elimina de forma segura la clave, si existe
            validated_data.pop(field, None) 
        
        # 3. Crear el objeto Jugador
        # Esto usará ahora los datos limpios + el objeto usuario
        jugador = Jugador.objects.create(usuario_id=usuario, **validated_data) 
        
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