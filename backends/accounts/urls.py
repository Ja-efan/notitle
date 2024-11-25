from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("like/", views.like_news, name='like_news'),
    path("is_liked/", views.is_news_liked, name='is_news_liked'),
    
]