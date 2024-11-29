def db_status(request):
    return {'db_status': getattr(request, 'db_status', 'unknown')}