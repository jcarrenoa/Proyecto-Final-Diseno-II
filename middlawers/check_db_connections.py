from django.db import connections
from django.db.utils import OperationalError

class CheckDatabaseConnectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            connections['default'].cursor()
            request.db_status = 'connected'
        except OperationalError:
            request.db_status = 'disconnected'
        return self.get_response(request)