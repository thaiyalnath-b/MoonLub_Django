from django.shortcuts import render
from django.urls import reverse_lazy

from django.contrib.auth.models import User

from django.contrib.auth.views import (
    LoginView
)

from django.views.generic import CreateView
# Create your views here.

class UserRegisterView(CreateView):
    model = User
    fields = ['username', 'password']
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('signin')

class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
