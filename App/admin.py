from django.contrib import admin
from .models import Card, Author, Recorrido,Linea, AboutInfo
# Register your models here.
admin.site.register(Card)
admin.site.register(Author)
admin.site.register(Recorrido)
admin.site.register(Linea)
admin.site.register(AboutInfo)