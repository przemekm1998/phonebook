from django.urls import path

from django.contrib.auth import views as auth_views
from .views import RegisterView, CustomLogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='users-register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),
         name='users-login'),
    path('logout/', CustomLogoutView.as_view(), name='users-logout'),
]
