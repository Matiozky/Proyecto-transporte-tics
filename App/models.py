from django.db import models
from django.db.models.base import Model
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
    mini_description = models.TextField(max_length=5000)
    color_tag = models.CharField(max_length=100,choices=COLOR_OPTIONS,default='bg-primary')
    img = models.ImageField()
    fuente = models.URLField(blank=True,null=True)
    autor = models.ForeignKey(Author,on_delete=models.CASCADE,blank=True,null=True)

    def get_absolute_url(self):
        return f"/aprende/{self.slug}"

    def __str__(self):
        return self.title


class RecorridoManager(models.Manager):
    
    def tiempo_sin_solucion(self, origen):
        lista_comunas=["Cerro Navia","El Bosque","La Granja","La Pintana","Lo Espejo","Maipú","Pedro Aguirre Cerda","Puente Alto","Pudahuel","Quilicura","Renca","San Bernardo"]
        tiempos_aproximados_del_10porciento_que_mas_tarda=[105,105,106,120,120,105,110,105,105,120,110,117]
        tiempos_aproximados_comuna_a_Santiago=[51,47,45,59,43,56,33,58,42,43,37,49]
        for i in range(0,12):
            if origen == lista_comunas[i]:
                tiempo_aproximado_de_traslado = (tiempos_aproximados_del_10porciento_que_mas_tarda[i] + tiempos_aproximados_comuna_a_Santiago[i])/2
                return tiempo_aproximado_de_traslado

    def tiempos_con_solucion(self, origen):
        lista_comunas2=["Cerro Navia","El Bosque","La Granja","La Pintana","Lo Espejo","Maipú","Pedro Aguirre Cerda","Puente Alto","Pudahuel","Quilicura","Renca","San Bernardo"]
        l=[]
        Estaciones_CN_Stgo=[0,0,1,0,0,0,0,8,0,0,0]
        segundostotales=[87,92,115,100,120,102,144,136,99,105,215]

        lineas = []

        def get_line(lista):
            lins = ['L1','L2','L3','L4','L4A','L5','L6','L7','L8','L9','METRO TREN']
            for i in range(0,len(lins)):
                if lista[i] != 0:
                    lineas.append(lins[i])




        if origen==lista_comunas2[0]:
            for j in range(len(segundostotales)):
                Tiempos_aproximados_solometro=Estaciones_CN_Stgo[j]*segundostotales[j]
                l.append(Tiempos_aproximados_solometro)
        elif origen==lista_comunas2[1]:
            for j in range(len(Estaciones_CN_Stgo)):
                Estaciones_EB_Stgo=[0,18,0,0,0,2,0,0,0,0,0] 
                Tiempos_aproximados_solometro=Estaciones_EB_Stgo[j]*segundostotales[j]
                get_line(Estaciones_EB_Stgo)
                l.append(Tiempos_aproximados_solometro)
        elif origen==lista_comunas2[2]:
            for j in range(len(Estaciones_CN_Stgo)):
                Estaciones_LG_Stgo=[0,0,1,0,1,5,0,0,0,7,0]
                Tiempos_aproximados_solometro=Estaciones_LG_Stgo[j]*segundostotales[j]
                get_line(Estaciones_LG_Stgo)
                l.append(Tiempos_aproximados_solometro)
        elif origen==lista_comunas2[3]:
            for j in range(len(Estaciones_CN_Stgo)):
                Estaciones_LP_Stgo=[1,0,1,0,0,0,0,0,0,13,0]
                Tiempos_aproximados_solometro=Estaciones_LP_Stgo[j]*segundostotales[j]
                get_line(Estaciones_LP_Stgo)
                l.append(Tiempos_aproximados_solometro)
        elif origen==lista_comunas2[4]:
            for j in range(len(Estaciones_CN_Stgo)):
                Estaciones_LE_Stgo=[5,0,1,0,0,0,0,0,0,0,4]
                Tiempos_aproximados_solometro=Estaciones_LE_Stgo[j]*segundostotales[j]
                get_line(Estaciones_LE_Stgo)
                l.append(Tiempos_aproximados_solometro)
        elif origen==lista_comunas2[5]:
            for j in range(len(Estaciones_CN_Stgo)):
                Estaciones_Ma_Stgo=[0,0,0,0,0,16,0,0,0,0,0]
                Tiempos_aproximados_solometro=Estaciones_Ma_Stgo[j]*segundostotales[j]
                get_line(Estaciones_Ma_Stgo)
                l.append(Tiempos_aproximados_solometro)
        elif origen==lista_comunas2[6]:
            for j in range(len(Estaciones_CN_Stgo)):
                Estaciones_PAC_Stgo=[5,0,1,0,0,0,0,0,0,0,3]
                Tiempos_aproximados_solometro=Estaciones_PAC_Stgo[j]*segundostotales[j]
                get_line(Estaciones_PAC_Stgo)
                l.append(Tiempos_aproximados_solometro)
        elif origen==lista_comunas2[7]:
            for j in range(len(Estaciones_CN_Stgo)):
                Estaciones_PA_Stgo=[0,0,9,18,0,0,0,0,0,0,0]
                Tiempos_aproximados_solometro=Estaciones_PA_Stgo[j]*segundostotales[j]
                get_line(Estaciones_PA_Stgo)
                l.append(Tiempos_aproximados_solometro)
        elif origen==lista_comunas2[8]:
            for j in range(len(Estaciones_CN_Stgo)):
                Estaciones_Pu_Stgo=[0,0,0,0,0,13,0,0,0,0,0] 
                Tiempos_aproximados_solometro=Estaciones_Pu_Stgo[j]*segundostotales[j]
                get_line(Estaciones_Pu_Stgo)
                l.append(Tiempos_aproximados_solometro)
        elif origen==lista_comunas2[9]:
            for j in range(len(Estaciones_CN_Stgo)):
                Estaciones_Qu_Stgo=[0,0,11,0,0,0,0,0,0,0,0] 
                Tiempos_aproximados_solometro=Estaciones_Qu_Stgo[j]*segundostotales[j]
                get_line(Estaciones_Qu_Stgo)
                l.append(Tiempos_aproximados_solometro)
        elif origen==lista_comunas2[10]:
            for j in range(len(Estaciones_CN_Stgo)):   ##REVISAR LO DE RENCA
                Estaciones_Re_Stgo=[0,0,4,0,0,0,0,10,0,0,0] 
                Tiempos_aproximados_solometro=Estaciones_Re_Stgo[j]*segundostotales[j]
                get_line(Estaciones_Re_Stgo)
                l.append(Tiempos_aproximados_solometro)
        elif origen==lista_comunas2[11]:
            for j in range(len(Estaciones_CN_Stgo)):
                Estaciones_SB_Stgo=[5,0,1,0,0,0,0,0,0,0,7] 
                Tiempos_aproximados_solometro=Estaciones_SB_Stgo[j]*segundostotales[j]
                get_line(Estaciones_SB_Stgo)
                l.append(Tiempos_aproximados_solometro)
        
        Tiempos_aproximados_moovit_solometro=[89,116,53,122,84,44,55,59,39,125,82,129]

        for i in range(0, 12):
            if origen == lista_comunas2[i]:
                tiempo_aproximado_con_solucion_solometro = (Tiempos_aproximados_moovit_solometro[i]+(sum(l)/60))/2



        return tiempo_aproximado_con_solucion_solometro, lineas
        

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



def producto_pre_save_reciver(sender, instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(producto_pre_save_reciver, sender = Recorrido)





def producto_pre_save_reciver(sender, instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(producto_pre_save_reciver, sender = Card)

