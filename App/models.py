from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import RESTRICT
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
    ('Plaza de armas','Plaza de armas'),
    ('Escuela Militar','Escuela Militar'),
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
comunas = [
    "Cerro Navia",
    "El Bosque",
    "La Granja",
    "La Pintana",
    "Lo Espejo",
    "Maipú",
    "Pedro Aguirre Cerda",
    "Puente Alto",
    "Pudahuel",
    "Quilicura",
    "Renca",
    "San Bernardo"
    ]


class Author(models.Model):
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=50, unique=True)
    profile_pic = models.ImageField()

    def __str__(self):
        return self.name


class Destino(models.Model):
    origen = models.CharField(max_length=150,choices=COMUNAS_CHOICES)
    destino = models.CharField(max_length=150, choices=DESTINOS_CHOICES)
    timestamp = DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.origen


class Card(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True,null=True,unique=True)
    mini_description = models.TextField(max_length=5000)
    color_tag = models.CharField(max_length=100,choices=COLOR_OPTIONS,default='bg-primary')
    img = models.ImageField()
    fuente = models.URLField(blank=True,null=True)
    autor = models.ForeignKey(Author,on_delete=models.CASCADE,blank=True,null=True)

    def get_absolute_url(self):
        return f"/aprende/{self.slug}"

    def __str__(self):
        return self.title


comunas = ["Cerro Navia","El Bosque","La Granja","La Pintana","Lo Espejo","Maipú","Pedro Aguirre Cerda","Puente Alto","Pudahuel","Quilicura","Renca","San Bernardo"]

class RecorridoManager(models.Manager):
    def create_object(self,lineas,origen,destino,solucion,solucion2):
        lns = []
        for i in lineas:
            if i not in lns:
                lns.append(i)

        new_obj = Recorrido.objects.create(title='trip',origen=origen,destino=destino,tiempo_con=str(solucion2),tiempo_sin=str(solucion))
        if new_obj is not None:
            new_obj.save()

        for i in lns:
            ln_obj = Linea.objects.get(title=i)
            if ln_obj is not None:
                new_obj.lineas.add(ln_obj)
                new_obj.save()
        return new_obj
    
    def tiempos_sin_plaza(self, origen):
        tiempos_maximos=[105,105,106,120,120,105,110,105,105,120,110,117]
        tiempos_minimos=[51,47,45,59,43,56,33,58,42,43,37,49]
        for i in range(0,12):
            if origen == comunas[i]:
                tiempo_medio = (tiempos_maximos[i] + tiempos_minimos[i])/2
                return tiempo_medio

    def tiempos_con_plaza(self, origen):
        tiempos_moovit=[89,116,53,122,84,44,55,59,39,125,82,129] 
        segundos = [87,92,115,100,120,102,144,136,99,105,215]
        estaciones = [ 
            [0,0,1,0,0,0,0,8,0,0,0],
            [0,18,0,0,0,2,0,0,0,0,0], 
            [0,0,1,0,1,5,0,0,0,7,0],
            [1,0,1,0,0,0,0,0,0,13,0],
            [1,0,1,0,0,0,0,0,0,13,0],
            [5,0,1,0,0,0,0,0,0,0,4],
            [0,0,0,0,0,16,0,0,0,0,0],
            [5,0,1,0,0,0,0,0,0,0,3],
            [0,0,9,18,0,0,0,0,0,0,0],
            [0,0,0,0,0,13,0,0,0,0,0],
            [0,0,11,0,0,0,0,0,0,0,0],
            [0,0,4,0,0,0,0,10,0,0,0],
            [5,0,1,0,0,0,0,0,0,0,7], 
        ]
        l2 = []
        lineas = []

        def get_line(lista):
            lins = ['L1','L2','L3','L4','L4A','L5','L6','L7','L8','L9','METRO TREN']
            for i in range(0,len(lins)):
                if lista[i] != 0:
                    lineas.append(lins[i])

        for i in range(0,len(comunas)):
            if origen == comunas[i]:
                for j in range(len(segundos)):
                    tiempo = estaciones[i][j]*segundos[j]
                    get_line(estaciones[i])
                    l2.append(tiempo)


        for i in range(0,12):
            if origen == comunas[i]:
                tiempo_sol = (tiempos_moovit[i]+(sum(l2)/60))/2

        return tiempo_sol, lineas

    def tiempos_sin_escuela(self, origen):
        tiempos_maximo=[105,105,106,120,120,105,110,105,105,120,110,117]
        tiemos_minimos=[67,55,66,87,64,61,59,58,65,59,52,83]

        for i in range(0,12):
            if origen == comunas[i]:
                tiempo_aproximado_de_traslado2 = (tiempos_maximo[i] + tiemos_minimos[i])/2
        return tiempo_aproximado_de_traslado2        
        
    def tiempos_con_escuela(self, origen):
        tiempos_moovit=[152,79,72,136,113,90,92,69,132,108,103,187]
        segundos=[87,92,115,100,120,102,144,136,99,105,110,215]
        estaciones = [
            [0,0,0,0,0,0,0,4,0,0,19,0], #cerro navia
            [3,5,0,12,5,0,0,0,0,0,0,0], #el bosque
            [3,0,0,12,3,0,0,0,0,0,0,0],
            [3,0,0,12,4,0,0,0,0,5,0,0],
            [3,0,0,12,5,0,0,0,0,0,1,0], # lo espejo
            [3,0,0,12,5,3,0,0,0,0,13,0],
            [0,0,0,0,0,0,8,4,0,0,0,0],
            [3,0,0,23,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,20,0], #pudahuel
            [0,0,4,0,0,0,0,0,0,0,19,0],
            [0,0,0,0,0,0,0,0,0,0,19,0], #renca
            [17,0,0,0,0,0,0,0,0,0,0,7],
        ]
        l2=[]
        lineas = []

        def get_line(lista):
            lins = ['L1','L2','L3','L4','L4A','L5','L6','L7','L8','L9','L10','METRO TREN']
            for i in range(0,len(lins)):
                if lista[i] != 0:
                    lineas.append(lins[i])


        for i in range(0,len(comunas)):
            if origen == comunas[i]:
                for j in range(len(segundos)):
                    tiempo = estaciones[i][j]*segundos[j]
                    get_line(estaciones[i])
                    l2.append(tiempo)


        for i in range(0,12):
            if origen == comunas[i]:
                tiempo_sol = (tiempos_moovit[i]+(sum(l2)/60))/2

        return tiempo_sol, lineas



class Linea(models.Model):
    title = models.CharField(max_length=200)
    img = models.ImageField(blank=True,null=True)

    def __str__(self):
        return self.title


class Recorrido(models.Model):
    title = models.CharField(max_length=200)
    origen = models.CharField(max_length=300)
    slug = models.SlugField(blank=True,null=True,unique=True)
    destino = models.CharField(max_length=300)
    tiempo_con = models.CharField(max_length=100)
    tiempo_sin = models.CharField(max_length=100)
    lineas = models.ManyToManyField(Linea,blank=True)

    objects = RecorridoManager()

    def __str__(self):
        return str(self.id)

class AboutInfo(models.Model):
    title = models.CharField(max_length=200)
    intro = models.TextField(max_length=5000)
    problema = models.TextField(max_length=5000)
    solucion = models.TextField(max_length=5000)

    def __str__(self):
        return self.title



def producto_pre_save_reciver(sender, instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(producto_pre_save_reciver, sender = Recorrido)





def producto_pre_save_reciver(sender, instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(producto_pre_save_reciver, sender = Card)

