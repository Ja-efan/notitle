from django.contrib import admin
from django.urls import path, include
from . import views

# api/v1/news/<str:id>/accounts/
urlpatterns = [
    path("like/", views.like_news, name='like_news'),
    path("is_liked/", views.is_news_liked, name='is_news_liked'),
    path("likes/", views.get_news_like, name='get_news_like'),
    # path('profile/', views.user_profile, name='user_profile'),
]