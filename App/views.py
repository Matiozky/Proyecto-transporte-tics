from django.shortcuts import render
from .forms import DestinoForm
from .models import Destino

# Create your views here.
def home(request):
    formulario = DestinoForm(request.POST or None)
    if request.method == "POST" and formulario.is_valid():
            origen = formulario.cleaned_data.get('origen')
            destino = formulario.cleaned_data.get('destino')
            print(origen)
            print(destino)
    ctx={
        'form': formulario
    }
    return render(request, 'App/home.html',ctx)

def about(request):
    ctx = {}
    return render(request,'App/about.html',ctx)