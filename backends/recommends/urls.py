from django.urls import path, include
from . import views

# 앱 네임스페이스 생성
app_name="news"
urlpatterns = [
    path('', views.recommended_news, name='recommended_news'),
]