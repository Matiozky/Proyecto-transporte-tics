from django.urls import path, re_path
from django.conf.urls import url
from . import views
urlpatterns = [
        path('', views.home, name = 'home'),
        path('lineas/',views.lines, name = 'lines'),
        path('about/', views.about, name='about'),
        path('your-travel/<slug:slug>/',views.info_view, name='info'),
        path('aprende/<slug:slug>/', views.CardSlugView.as_view(), name="slugview"),
    ]
