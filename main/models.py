from django.db import models

class Log(models.Model):
    TIPO_TRANSACCION = [
        ('CONSULTAR', 'Consultar'),
        ('ELIMINAR', 'Eliminar'),
        ('EDITAR', 'Editar'),
        ('CREAR', 'Crear'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_TRANSACCION)
    documento = models.CharField(max_length=255)  # Ej. ID, número, etc.
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de la transacción
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.documento} - {self.fecha}"