from django.urls import path, include
from . import views

# 앱 네임스페이스 생성
app_name="news"
urlpatterns = [
    # name: 경로를 직접 사용하지 않고,
    #   이름으로 쓰기 위해서 설정
    # api/v1/
    path('', views.news_list, name="news_list"),
    path("news/<str:id>/", views.news_detail, name='news_detail'),
    path("news/<str:id>/accounts/", include('accounts.urls')),
    path("news-analysis/", views.news_analysis, name='news_analysis'),
    path("recommended-news/", include('recommends.urls')),
    path("liked-news/", views.liked_news, name='liked_news'),
    path('get-categories/', views.get_categories, name='get_categories'),
]
