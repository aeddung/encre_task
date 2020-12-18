from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
path('board_list', views.board_list),
path('<int:board_id>', views.board_update),
]