from django.shortcuts import render
from auth_mysite.models import Persona
from bot.bot import Bot
from .forms import PersonaForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Log
from django.views.generic import ListView

bot = Bot()

def main_view(request):
    personas = Persona.objects.all()
    return render(request, 'main.html', {'personas': personas})

@login_required
def detalles_view(request, id):
    persona = Persona.objects.get(id=id)
    etimologia = bot.get_response(persona.primer_nombre)
    registrar_log('CONSULTAR', persona.nro_documento)
    return render(request, 'detalles.html', {'persona': persona, 'etimologia': etimologia})

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
    template_name = 'loglist.html'  # Ruta del template
    context_object_name = 'logs'  # Nombre del objeto en el contexto
    paginate_by = 10  # Número de logs por página

    def get_queryset(self):
        # Recuperamos el queryset
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # Capturar la búsqueda de la URL
        if query:
            # Filtramos los logs por el documento que contenga el término de búsqueda
            queryset = queryset.filter(documento__icontains=query)
        return queryset