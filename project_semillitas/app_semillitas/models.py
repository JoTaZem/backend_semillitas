from django.db import models
from django.contrib.auth.models import AbstractUser

roles = [('Admin','Admin'),('Jugador','Jugador'),]
evaluaciones = [('ahorcado','Ahorcado'),('pares','Pares'),('union','Union'),]


class Usuario(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True) # Mantener unique para evitar duplicados
    fecha_nacimiento = models.DateField(null=False)
    rol = models.CharField(max_length=20, choices = roles)
    def __str__(self):
        return self.username

class Administrador(models.Model):    
    usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT) 
    def __str__(self):
        return f"{self.usuario.username}"
    
class Jugador(models.Model):    
    usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT) 
    def __str__(self):
        return f"{self.usuario.username}"   

    
class Nivel(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion =  models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Palabra(models.Model):
    pal_español = models.CharField(max_length=50,unique=True)
    pal_ampiu =  models.CharField(max_length=50,unique=True)
    nivel = models.ForeignKey(Nivel, on_delete=models.PROTECT)   
    def __str__(self):
        return self.pal_español
    
class Evaluacion(models.Model):
    nombre = models.CharField(max_length=50,default="")
    descripcion = models.CharField(max_length=50,default="")
    tipo=models.CharField(max_length=20, choices = evaluaciones)
    nivel =  models.ForeignKey(Nivel, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nivel.nombre
    
class UsuarioPalabras(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT)
    palabra = models.ForeignKey(Palabra,on_delete=models.PROTECT)
    fecha_recogida = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.fecha_recogida
    
class Pregunta(models.Model):
    evaluacion=models.ForeignKey(Evaluacion,on_delete=models.PROTECT)
    palabra = models.ForeignKey(Palabra,on_delete=models.PROTECT)
    enunciado = models.CharField(max_length=100)
    respuesta_correcta = models.CharField(max_length=25)
    respuesta_usuario = models.CharField(max_length=25)
    acierta = models.BooleanField()
    def __str__(self):
        return self.enunciado
    
class EvaluacionUsuarios(models.Model):
    evaluacion = models.ForeignKey(Evaluacion,on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT)
    fecha =models.DateTimeField(auto_now_add=True)

class ResultadoEvaluaciones(models.Model):
    evaluacion = models.ForeignKey(Evaluacion,on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario,on_delete=models.PROTECT)
    puntaje = models.IntegerField(default=150)
    completado = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)