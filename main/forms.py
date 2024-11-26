from django import forms
from auth_mysite.models import Persona
import re

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['primer_nombre', 'segundo_nombre', 'apellidos', 'tipo_documento', 'nro_documento',
                  'fecha_nacimiento', 'genero', 'correo', 'celular', 'foto_identificacion']
        widgets = {
            'primer_nombre': forms.TextInput(),
            'segundo_nombre': forms.TextInput(),
            'apellidos': forms.TextInput(),
            'tipo_documento': forms.Select(),
            'nro_documento': forms.TextInput(),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'genero': forms.Select(),
            'correo': forms.EmailInput(),
            'celular': forms.TextInput(),
            'foto_identificacion': forms.ClearableFileInput(),
        }

    def clean_primer_nombre(self):
        primer_nombre = self.cleaned_data.get('primer_nombre')
        if not re.match(r'^[A-Za-zÑñÁáÉéÍíÓóÚú\s]+$', primer_nombre):
            raise forms.ValidationError('El primer nombre debe contener solo letras.')
        return primer_nombre

    def clean_segundo_nombre(self):
        segundo_nombre = self.cleaned_data.get('segundo_nombre')
        if segundo_nombre and not re.match(r'^[A-Za-zÑñÁáÉéÍíÓóÚú\s]+$', segundo_nombre):
            raise forms.ValidationError('El segundo nombre debe contener solo letras.')
        return segundo_nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not re.match(r'^[A-Za-zÑñÁáÉéÍíÓóÚú\s]+$', apellidos):
            raise forms.ValidationError('Los apellidos deben contener solo letras.')
        return apellidos
    
    def clean_celular(self):
        celular = self.cleaned_data.get('celular')
        if not str(celular).isdigit():  # Verifica que solo contenga números
            raise forms.ValidationError('El celular debe contener solo números.')
        return celular

    def clean_nro_documento(self):
        nro_documento = self.cleaned_data.get('nro_documento')
        if not str(nro_documento).isdigit():  # Verifica que solo contenga números
            raise forms.ValidationError('El número de documento debe contener solo números.')
        return nro_documento
    
    def clean_foto_identificacion(self):
        foto = self.cleaned_data.get('foto_identificacion')
        if foto and type(foto) != str:
            max_size_mb = 10  # Tamaño máximo en MB (10 MB)
            if foto.size > max_size_mb * 1024 * 1024:  # Convertir MB a bytes
                raise forms.ValidationError(f'La foto no debe exceder {max_size_mb} MB.')
        return foto