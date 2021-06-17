from django.shortcuts import render, get_object_or_404
from .forms import DestinoForm
from django.http import Http404
from .models import Destino, Card
from django.views.generic import DetailView


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
