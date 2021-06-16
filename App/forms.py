from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import ChoiceField
from .models import Destino

class DestinoForm(forms.ModelForm):
    class Meta:
        model = Destino
        fields = ['origen','destino'] 
        widgets = {
            'origen': widgets.Select(attrs={'class': 'form-select','id':'floatingSelect'}),
            'destino': widgets.Select(attrs={'class': 'form-select','id':'floatingSelect'}),
        }
