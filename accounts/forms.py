from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from newsportal.models import Author


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
    def save_addgroup(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        return user

    # def add_author(self, request, username=None):
    #     if request.method == 'POST':
    #         user_form = SignupForm(request.POST)
    #         if user_form.is_valid():
    #             new_author = Author.objects.create(name=username)
    #             new_author.save()
    #
