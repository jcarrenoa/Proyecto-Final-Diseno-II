from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [	
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]