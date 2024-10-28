from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.core.mail import send_mail, mail_managers


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

    def save(self, request):
        # Метод отправки письма на почту при регистрации пользователя
        user = super().save(request)

        send_mail(
            subject='Добро пожаловать в наш интернет-магазин!', # Тема письма
            message=f'{user.username}, вы успешно зарегистрировались!', # Содержание письма
            from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
            recipient_list=[user.email], # почтовый адрес
        )

        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )
        return user

    def save_addgroup(self, request):
        # Метод для добавление пользователя в группу "common users"
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        return user
