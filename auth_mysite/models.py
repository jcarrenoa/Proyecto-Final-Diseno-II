from django.db import models

class Persona(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
    ]

    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('NB', 'No binario'),
        ('N/A', 'Prefiero no decirlo'),
    ]

    # Campos del formulario
    primer_nombre = models.CharField(max_length=30, blank=False)
    segundo_nombre = models.CharField(max_length=30, blank=True)  # Segundo nombre opcional
    apellidos = models.CharField(max_length=60, blank=False)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES, blank=False)
    nro_documento = models.CharField(max_length=10, unique=True, blank=False)  # El número de documento debe ser único
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=3, choices=GENERO_CHOICES, blank=False)
    correo = models.EmailField(unique=True, blank=False)  # El correo debe ser único
    celular = models.CharField(max_length=10, blank=False)
    foto_identificacion = models.ImageField(upload_to='perfil/%Y/%m/%d', default='perfil/iconuser.png')  # Foto opcional

    def __str__(self):
        return f'{self.primer_nombre} {self.apellidos}'

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
