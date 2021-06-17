from django.db import models
from django.db.models.fields import DateTimeField, TimeField
from django.db.models.signals import pre_save
from .utils import unique_slug_generator

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

COLOR_OPTIONS = [
    ('bg-primary','bg-primary'),
    ('bg-secondary','bg-secondary'),
    ('bg-success','bg-success'),
    ('bg-danger','bg-danger'),
    ('bg-warning','bg-warning'),
    ('bg-info','bg-info'),
    ('bg-light','bg-light'),
    ('bg-dark','bg-dark'),
    ('bg-orange','bg-orange'),
    ('bg-brown','bg-brown'),
    ('bg-purple','bg-purple'),
    ('bg-magenta','bg-magenta'),


]

class Author(models.Model):
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=50, unique=True)
    profile_pic = models.ImageField()

    def __str__(self):
        return self.name


class Destino(models.Model):
    origen = models.CharField(max_length=150,choices=COMUNAS_CHOICES)
    destino = models.CharField(max_length=150, choices=DESTINOS_CHOICES, default='Centro de Santiago')
    timestamp = DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.origen


class Card(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True,null=True,unique=True)
    mini_description = models.TextField(max_length=200)
    color_tag = models.CharField(max_length=100,choices=COLOR_OPTIONS,default='bg-primary')
    img = models.ImageField()
    fuente = models.URLField(blank=True,null=True)
    autor = models.ForeignKey(Author,on_delete=models.CASCADE,blank=True,null=True)

    def get_absolute_url(self):
        return f"/aprende/{self.slug}"

    def __str__(self):
        return self.title

def producto_pre_save_reciver(sender, instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(producto_pre_save_reciver, sender = Card)

