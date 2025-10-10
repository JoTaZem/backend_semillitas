from django.db import models
from django.contrib.auth.models import AbstractUser
roles = [
    ('Admin','Admin'),
    ('Jugador','Jugador'),
]

class Usuario(AbstractUser):
    username = models.CharField(max_length=80,unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices = roles)
    def __str__(self):
        return self.username
class Jugador(models.Model):
    user_id= models.ForeignKey(Usuario,on_delete=models.PROTECT)
    fecha_nacimiento = models.DateField()
    def __str__(self):
        return f"{self.user_id.username}"    
class Nivel(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion =  models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Palabra(models.Model):
    pal_español = models.CharField(max_length=50,unique=True)
    pal_ampiu =  models.CharField(max_length=50,unique=True)
    nivel_id = models.ForeignKey(Nivel, on_delete=models.PROTECT)   
    def __str__(self):
        return self.pal_español
    
class Evaluacion(models.Model):
    usuario_id =  models.ForeignKey(Usuario, on_delete=models.PROTECT)
    nivel_id =  models.ForeignKey(Nivel, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    puntaje = models.IntegerField()
    def __str__(self):
        return self.nivel_id.nombre
    
class usuario_palabras(models.Model):
    usuario_id = models.ForeignKey(Usuario,on_delete=models.PROTECT)
    palabra_id = models.ForeignKey(Palabra,on_delete=models.PROTECT)
    fecha_recogida = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.fecha_recogida
    
class Pregunta(models.Model):
    evaluacion_id=models.ForeignKey(Evaluacion,on_delete=models.PROTECT)
    palabra_id = models.ForeignKey(Palabra,on_delete=models.PROTECT)
    enunciado = models.CharField(max_length=100)
    respuesta_correcta = models.CharField(max_length=25)
    respuesta_usuario = models.CharField(max_length=25)
    acierta = models.BooleanField()
    def __str__(self):
        return self.enunciado
    
