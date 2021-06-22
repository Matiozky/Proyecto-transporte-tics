from django.db import models
from django.db.models.base import Model
from django.shortcuts import redirect, render, get_object_or_404
from .forms import DestinoForm
from django.http import Http404
from .models import Card, Recorrido, AboutInfo
from django.views.generic import DetailView


# Create your views here.
def home(request):
    formulario = DestinoForm(request.POST or None)
    if request.method == "POST" and formulario.is_valid():
            origen = formulario.cleaned_data.get('origen')
            destino = formulario.cleaned_data.get('destino')

            if destino == "Plaza de armas":
                solucion = Recorrido.objects.tiempos_sin_plaza(origen)
                solucion2,lineas = Recorrido.objects.tiempos_con_plaza(origen)

                new_obj = Recorrido.objects.create_object(lineas,origen,destino,solucion,solucion2)

                return redirect(f'/your-travel/{new_obj.slug}')

            elif destino == "Escuela Militar":
                solucion = Recorrido.objects.tiempos_sin_escuela(origen)
                solucion2,lineas = Recorrido.objects.tiempos_con_escuela(origen)
                print(lineas)

                new_obj = Recorrido.objects.create_object(lineas,origen,destino,solucion,solucion2)


                return redirect(f'/your-travel/{new_obj.slug}')

    ctx={
        'form': formulario
    }
    return render(request, 'App/home.html',ctx)


def info_view(request,slug):
    obj = Recorrido.objects.get(slug=slug)
    ctx={
        'instance':obj
    }
    return render(request, 'App/info_view.html',ctx)


def lines(request):
    obj = Card.objects.all()
    ctx={
        'object':obj,
    }
    return render(request, 'App/lineas.html',ctx)


class CardSlugView(DetailView):
    queryset = Card.objects.all()
    template_name = 'App/articulo.html'

    def get_context_data(self,*args, **kwargs):
        context = super(CardSlugView, self).get_context_data(*args,**kwargs)
        request = self.request
        context['redirect_url'] = 'slugview'
        return context

    def get_object(self, *args, **kwargs):
        request=self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Card, slug=slug)

        if instance is None:
            raise Http404("El Articulo no existe")
        return instance


def about(request):
    obj = AboutInfo.objects.get(title = 'Oficial')
    ctx = {
        'object':obj
    }
    return render(request,'App/about.html',ctx)
