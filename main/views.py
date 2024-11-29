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
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

bot = Bot()

@login_required
def main_view(request):
    try:
        response = requests.get('http://localhost:5000/persona', timeout=3)
        if response.status_code == 200:
            try:
                personas = response.json() 
            except ValueError:  
                return HttpResponse("Error: La respuesta no es un JSON válido.", status=500)
            return render(request, 'main.html', {'personas': personas})
        else:
            return HttpResponse(f"Error: El servicio respondió con el código {response.status_code}.", status=500)
    except requests.exceptions.ConnectionError:
        return HttpResponse("Error: No se pudo conectar con el servicio Flask.", status=500)
    except requests.exceptions.Timeout:
        return HttpResponse("Error: Tiempo de espera agotado al intentar conectar con el servicio.", status=500)
    except Exception as e:
        # Capturar cualquier otro error no anticipado
        return HttpResponse(f"Error inesperado: {str(e)}", status=500)

@login_required
def detalles_view(request, id):
    try:
        response = requests.get(f'http://localhost:5000/persona/{id}', timeout=3)
        if response.status_code == 200:
            try:
                persona = response.json()
            except ValueError:
                return HttpResponse("Error: La respuesta no es un JSON válido.", status=500)
            etimologia = bot.get_response(persona["primer_nombre"])
            registrar_log('CONSULTAR', persona["nro_documento"])
            return render(request, 'detalles.html', {**persona, 'etimologia': etimologia})
        else:
            return HttpResponse(f"Error: El servicio respondió con el código {response.status_code}.", status=500)
    except requests.exceptions.ConnectionError:
        return HttpResponse("Error: No se pudo conectar con el servicio Flask.", status=500)
    
    except requests.exceptions.Timeout:
        return HttpResponse("Error: Tiempo de espera agotado al intentar conectar con el servicio.", status=500)
    
    except Exception as e:
        return HttpResponse(f"Error inesperado: {str(e)}", status=500)

@login_required
def register(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Guarda el registro en la base de datos
            registrar_log('CREAR', form.cleaned_data['nro_documento'])
            form = PersonaForm()
            response = requests.get('http://localhost:5000/persona', timeout=3)
            personas = response.json()
            return render(request, 'main.html', {'personas': personas})  # Redirige a una vista de lista o a otra página después de guardar
    else:
        form = PersonaForm()
    return render(request, 'register.html', {'form': form})

@login_required
def editar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)

    if request.method == 'POST':
        form = PersonaForm(request.POST, request.FILES, instance=persona)
        if form.is_valid():
            form.save()
            return redirect('main_view')
    else:
        form = PersonaForm(instance=persona)

    return render(request, 'editar_persona.html', {'form': form})

@login_required
def eliminar_persona(request, persona_id):
    response = requests.get(f'http://localhost:5000/persona/{persona_id}', timeout=3)
    if response.status_code == 200:
        try:
            persona = response.json()
            if request.method == 'POST':
                response = requests.delete(f'http://localhost:5000/persona/{persona_id}', timeout=3)
                registrar_log('ELIMINAR', persona["nro_documento"])
                print(f"Codigo de eestado: {response.status_code}")
                return redirect('main_view')
            return render(request, 'editar_persona.html', {'persona': persona})
        except ValueError:
            return HttpResponse("Error: La respuesta no es un JSON válido.", status=500)

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