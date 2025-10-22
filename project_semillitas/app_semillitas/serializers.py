from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  
from .models import *
from django.db import transaction


class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = '__all__'
    def create(self, validated_data):
        nivel = Nivel.objects.create(**validated_data)
        return nivel

class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = '__all__'
    def create(self, validated_data):
        evaluacion = Evaluacion.objects.create(**validated_data)
        return evaluacion

class PalabraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palabra
        fields = '__all__'
    def create(self, validated_data):
        palabra = Palabra.objects.create(**validated_data)
        return palabra

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        depth = 2
        extra_kwargs = {'password' :{'write_only': True, 'required':False},
            'first_name': {'required': False},
            'username':{'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'rol':{'required':False},
            'fecha_nacimiento': {'required': True}
        }
    def create(self,validated_data):
        user =  Usuario(**validated_data)
        password = validated_data.get('password')
        if password and password.strip():
            user.set_password(password)
        user.save()
        return user
    
class AdminSerializer(serializers.ModelSerializer):
    usuario=UsuariosSerializer()
    class Meta: 
        model = Administrador
        fields = '__all__'
    def create(self,validated_data):
        usuario_data = validated_data.pop('usuario')
        username = usuario_data.get('email')
        if not username:
            raise serializers.ValidationError({"email": "El correo es obligatorio para el Administrador."})
        usuario_data['username'] = username
        usuario_data['rol'] = 'Admin'
        Usuario = UsuariosSerializer().create(usuario_data) 
        admin = Administrador.objects.create(usuario=Usuario,**validated_data)
        return admin
    
class JugadorSerializer(serializers.ModelSerializer):
    usuario=UsuariosSerializer()
    class Meta: 
        model = Jugador
        fields = '__all__'
    def create(self,validated_data):
        usuario_data = validated_data.pop('usuario')
        jugador_nombre = usuario_data.get('username')
        if not jugador_nombre:
            raise serializers.ValidationError({"username": "El nombre de usuario es obligatorio para el Jugador."})
 
        usuario_data['password'] = jugador_nombre
        usuario_data['rol'] = 'Jugador'
        Usuario = UsuariosSerializer().create(usuario_data)
        jugador = Jugador.objects.create(usuario=Usuario,**validated_data)        
        return jugador  
        #usuario = UsuariosSerializer().create(usuario_data) 
        #jugador = Jugador.objects.create(usuario_id=usuario,**validated_data)        
        #return jugador  

class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = '__all__'
    def create(self, validated_data):
        ejercicio = Ejercicio.objects.create(**validated_data)
        return ejercicio

class UsuarioPalabrasSerializer(serializers.ModelSerializer):
    class Meta:
        model=UsuarioPalabras
        fields='__all__'
    def create(self, validated_data):       
        usuarioPalabras = UsuarioPalabras.objects.create(**validated_data)
        return usuarioPalabras
    
class EvaluacionUsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionUsuarios
        fields = '__all__'
    def create(self, validated_data):
        evaluacion_usuario = EvaluacionUsuarios.objects.create(**validated_data)
        return evaluacion_usuario


class ResultadoEvaluacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoEvaluaciones
        fields = '__all__'

    def create(self, validated_data):
        resultado = ResultadoEvaluaciones.objects.create(**validated_data)
        return resultado

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