from django.shortcuts import render
from auth_mysite.models import Persona
from bot.bot import Bot

bot = Bot()

def main_view(request):
    personas = Persona.objects.all()
    return render(request, 'main.html', {'personas': personas})

def detalles_view(request, id):
    persona = Persona.objects.get(id=id)
    etimologia = bot.get_response(persona.primer_nombre)
    print(etimologia)
    return render(request, 'detalles.html', {'persona': persona, 'etimologia': etimologia})