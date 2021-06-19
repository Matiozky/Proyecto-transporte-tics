from django.shortcuts import redirect, render, get_object_or_404
from .forms import DestinoForm
from django.http import Http404
from .models import Destino, Card, Recorrido, Linea
from django.views.generic import DetailView


# Create your views here.
def home(request):
    formulario = DestinoForm(request.POST or None)
    if request.method == "POST" and formulario.is_valid():
            origen = formulario.cleaned_data.get('origen')
            destino = formulario.cleaned_data.get('destino')
            solucion = Recorrido.objects.tiempo_sin_solucion(origen)
            solucion2,lineas = Recorrido.objects.tiempos_con_solucion(origen)

            lns = []
            for i in lineas:
                if i not in lns:
                    lns.append(i)

            new_obj = Recorrido.objects.create(title='trip',origen=origen,destino=destino,tiempo_con=str(solucion2),tiempo_sin=str(solucion))
            if new_obj is not None:
                new_obj.save()

            for i in lns:
                ln_obj = Linea.objects.get(title=i)
                print(ln_obj)
                if ln_obj is not None:
                    new_obj.lineas.add(ln_obj)
                    new_obj.save()


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
    ctx = {}
    return render(request,'App/about.html',ctx)
