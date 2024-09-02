from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView
from .forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse


class SignUp(CreateView):
    '''Регистрация пользователей'''
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

class ProfileList(LoginRequiredMixin,ListView):
    '''Профиль пользователя'''
    template_name = 'auth/profile.html'
    context_object_name = 'users'
    queryset = User.objects.all()


def key(request):
    id_user = request.GET[id]
    return HttpResponse(f""" id: {id_user}
""")

