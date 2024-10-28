from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    '''Данные пользователя для профиля'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=4, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to='user_images',
                              default='user_images/default-user.png')