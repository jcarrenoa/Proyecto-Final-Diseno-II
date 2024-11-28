from django import forms
from .models import Persona

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'primer_nombre', 'segundo_nombre', 'apellidos', 'tipo_documento', 
            'nro_documento', 'fecha_nacimiento', 'genero', 'correo', 'celular', 
            'foto_identificacion',
        ]
    widgets = {
        'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
    }
