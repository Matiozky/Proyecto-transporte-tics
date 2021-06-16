from django.urls import path, re_path
from django.conf.urls import url
from . import views
urlpatterns = [
        path('home/', views.home, name = 'home'),
        path('about/', views.about, name='about'),
        
    ]
