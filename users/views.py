from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import UserRegisterForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('users-login')
    template_name = 'users/register.html'


class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'
