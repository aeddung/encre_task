from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('create', views.Registration.as_view()),
    path('login', views.Login.as_view()),
    path('active', views.Active.as_view()),
    path('game-list', views.GameList.as_view()),
    path('game', views.GamePost.as_view()),
    path('game-update/<int:pk>', views.GameUpdate.as_view()),
    path('character-list', views.CharacterList.as_view()),
    path('character', views.CharacterPost.as_view()),
    path('character-detail/<str:name>', views.CharacterDetail.as_view()),
    path('character-update/<str:name>', views.CharacterUpdate.as_view()),
    path('comment-list', views.CommentList.as_view()),
    path('comment', views.CommentPost.as_view()),
    path('comment-update/<int:pk>', views.CommentUpdate.as_view()),
]