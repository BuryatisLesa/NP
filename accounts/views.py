from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView
from .forms import SignupForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse


class SignUp(CreateView):
    '''Регистрация пользователей'''
    model = User
    form_class = SignupForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'








