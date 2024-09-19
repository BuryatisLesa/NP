from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.core.mail import send_mail


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )


class CustomSignupForm(SignupForm):
    """Форма регистрации из пакета - allauth"""
    def send_sms(self, request):
        # метод для отправки письма при регистрации пользователя
        user = super().save(request)

        send_mail(
            subject='Добро пожаловать в "AnimeNews"!',
            message=f'{user.username}, Вы успешно зарегистрировались',
            from_email=None,  # DEFAULT_FROM_EMAIL
            recipient_list=[user.email]
        )
        return user

    def save_addgroup(self, request):
        # метод для добавление пользователя в группу "common users"
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        return user