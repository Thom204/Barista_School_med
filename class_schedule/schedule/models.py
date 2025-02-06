import json
from django.db import models
# Create your models here.
class Clase(models.Model):
    fecha = models.DateField()
    hora = models.TextField()
    profesores = models.TextField()  # Guardaremos como JSON
    alumnos = models.TextField()  # Guardaremos como JSON

    def get_profesores(self):
        return json.loads(self.profesores)

    def get_alumnos(self):
        return json.loads(self.alumnos)

    def __str__(self):
        return f"Clase {self.fecha} {self.hora}"
