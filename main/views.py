from django.shortcuts import render
from auth_mysite.models import Persona
from bot.bot import Bot
from .forms import PersonaForm, LogSearchForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Log
from django.views.generic import ListView
import requests

bot = Bot()

def main_view(request):
    personas = Persona.objects.all()
    return render(request, 'main.html', {'personas': personas})

@login_required
def detalles_view(request, id):
    response = requests.get(f'http://localhost:5000/persona/{id}')
    if response.status_code == 200:
        persona = response.json()
        etimologia = bot.get_response(persona["primer_nombre"])
        registrar_log('CONSULTAR', persona["nro_documento"])
        return render(request, 'detalles.html', {**persona, 'etimologia': etimologia})

@login_required
def register(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Guarda el registro en la base de datos
            registrar_log('CREAR', form.cleaned_data['nro_documento'])
            form = PersonaForm()
            return render(request, 'register.html', {'form': form})  # Redirige a una vista de lista o a otra página después de guardar
    else:
        form = PersonaForm()
    return render(request, 'register.html', {'form': form})

def exit(request):
    logout(request)
    return redirect('/')

def registrar_log(tipo, documento):
    """Función para registrar logs."""
    Log.objects.create(tipo=tipo, documento=documento)

class LogListView(ListView):
    model = Log
    template_name = 'loglist.html'
    context_object_name = 'logs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query_params = self.request.GET
        form = LogSearchForm(query_params)
        
        if form.is_valid():
            # Filtrar por documento
            documento = form.cleaned_data.get('documento')
            if documento:
                queryset = queryset.filter(documento__icontains=documento)

            # Filtrar por tipo
            tipo = form.cleaned_data.get('tipo')
            if tipo:
                queryset = queryset.filter(tipo=tipo)

            # Filtrar por rango de fechas
            fecha_inicio = form.cleaned_data.get('fecha_inicio')
            fecha_fin = form.cleaned_data.get('fecha_fin')
            if fecha_inicio and fecha_fin:
                queryset = queryset.filter(fecha__date__range=[fecha_inicio, fecha_fin])
            elif fecha_inicio:
                queryset = queryset.filter(fecha__date__gte=fecha_inicio)
            elif fecha_fin:
                queryset = queryset.filter(fecha__date__lte=fecha_fin)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos TIPO_CHOICES al contexto para que el template lo reciba
        context['tipos'] = Log.TIPO_TRANSACCION
        return context