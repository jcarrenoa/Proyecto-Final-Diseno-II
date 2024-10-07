from django.shortcuts import render
from auth_mysite.models import Persona

def main_view(request):
    personas = Persona.objects.all()
    return render(request, 'main.html', {'personas': personas})

def detalles_view(request, id):
    persona = Persona.objects.get(id=id)
    return render(request, 'detalles.html', {'persona': persona})