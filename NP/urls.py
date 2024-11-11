"""
URL configuration for NP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from allauth import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    # path('accounts/', include('django.contrib.auth.urls'), name='account_login'),
    # path("accounts/", include("accounts.urls"), name='account_logout'),
    path("accounts/", include("allauth.urls")),
    # accounts/ login/ [name='account_login']
    # accounts/ logout/ [name='account_logout']
    # accounts/ inactive/ [name='account_inactive']
    # accounts/ signup/ [name='account_signup']
    # accounts/ reauthenticate/ [name='account_reauthenticate']
    # accounts/ email/ [name='account_email']
    # accounts/ confirm-email/ [name='account_email_verification_sent']
    # accounts/ ^confirm-email/(?P<key>[-:\w]+)/$ [name='account_confirm_email']
    # accounts/ password/change/ [name='account_change_password']
    # accounts/ password/set/ [name='account_set_password']
    # accounts/ password/reset/ [name='account_reset_password']
    # accounts/ password/reset/done/ [name='account_reset_password_done']
    # accounts/ ^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$ [name='account_reset_password_from_key']
    # accounts/ password/reset/key/done/ [name='account_reset_password_from_key_done']
    # accounts/ login/code/confirm/ [name='account_confirm_login_code']
    # accounts/ 3rdparty/
    # accounts/ social/login/cancelled/
    # accounts/ social/login/error/
    # accounts/ social/signup/
    # accounts/ social/connections/
    # accounts/ yandex/
    path('',include('newsportal.urls')),
    path('board/',include('board.urls')),
    # path('accounts/', include('accounts.urls'))
    path('i18n/', include('django.conf.urls.i18n')), # локализация

]
