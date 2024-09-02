from django.urls import path
from .views import SignUp, ProfileList
# from accounts import views

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('profile/', ProfileList.as_view(), name='profile'),
]