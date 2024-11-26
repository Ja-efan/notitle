from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserActivity
from news.models import News
from news.serializers import NewsSerializer
from django.db.models import Count

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def recommended_news(request):
    user = request.user

    # 1. 사용자가 좋아요를 누른 뉴스 카테고리 가져오기
    liked_categories = UserActivity.objects.filter(
        user=user, action_type='like'
    ).values_list('news__category', flat=True)

    # 2. 동일 카테고리의 뉴스 추천 (단, 사용자가 좋아요 하지 않은 뉴스만)
    recommended_news = News.objects.filter(
        category__in=liked_categories
    ).exclude(
        user_activities__user=user
    )[:10]

    # 3. 사용자가 좋아요를 누른 뉴스 가져오기
    liked_news = News.objects.filter(
        user_activities__user=user, user_activities__action_type='like'
    )

    # 4. 좋아요 누른 뉴스 분석 정보
    liked_news_analysis = {
        "total_liked": liked_news.count(),
        "categories_distribution": liked_news.values('category__category_name').annotate(count=Count('article_id')),
        "sentiment_distribution": {
            "positive": liked_news.filter(sentiment_score__gt=0).count(),
            "neutral": liked_news.filter(sentiment_score=0).count(),
            "negative": liked_news.filter(sentiment_score__lt=0).count(),
        },
    }

    # Serialize 데이터를 반환
    serializer = NewsSerializer(recommended_news, many=True)
    return Response({
        "recommended_news": serializer.data,
        "liked_news_analysis": liked_news_analysis
    }, status=status.HTTP_200_OK)


