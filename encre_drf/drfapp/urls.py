from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('create', views.createUser),
    path('login', views.login),
]