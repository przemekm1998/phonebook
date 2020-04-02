from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegisterForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('users-login')
    template_name = 'users/register.html'
