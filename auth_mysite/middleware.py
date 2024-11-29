from django.db import OperationalError
from django.shortcuts import render

class HandleDatabaseErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except OperationalError as e:
            # Renderizar una página de error personalizada
            return render(request, 'error_database.html', {"error": str(e)}, status=500)
        return response