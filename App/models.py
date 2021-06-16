from django.db import models
from django.db.models.fields import DateTimeField, TimeField

# Create your models here.

COMUNAS_CHOICES = [
    ('Cerro Navia','Cerro Navia'),
    ('El Bosque','El Bosque'),
    ('Maipú','Maipú'),
    ('Pudahuel','Pudahuel'),
    ('Puente Alto','Puente Alto'),
    ('La Granja','La Granja'),
    ('Pedro Aguirre Cerda','Pedro Aguirre Cerda'),
    ('Renca','Renca'),
    ('San Bernardo','San Bernardo'),
    ('La Pintana','La Pintana'),
    ('Lo Espejo','Lo Espejo'),
    ('Quilicura','Quilicura'),

]
DESTINOS_CHOICES =[
    ('Centro de Santiago','Centro de Santiago'),
]


class Destino(models.Model):
    origen = models.CharField(max_length=150,choices=COMUNAS_CHOICES)
    destino = models.CharField(max_length=150, choices=DESTINOS_CHOICES, default='Centro de Santiago')
    timestamp = DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.origen