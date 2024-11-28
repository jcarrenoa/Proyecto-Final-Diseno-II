"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .views import LogListView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', login_required(views.main_view), name='main_view'),
    path('detalles/<int:id>/', views.detalles_view, name='detalles'),
    path('exit/', views.exit, name='exit'),
    path('logs/', login_required(LogListView.as_view()), name='log_list'),
    path('editar/<int:persona_id>/', views.editar_persona, name='editar_persona'),
    path('eliminar/<int:persona_id>/', views.eliminar_persona, name='eliminar_persona')
]
