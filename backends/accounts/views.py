from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import UserActivity
from news.models import News

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능 
def like_news(request, id):
    user = request.user
    # if not user.is_authenticated:
    #     return Response({'error': '로그인이 필요합니다.'}, status=401)

    # news_id = id
    print(f"{user}이(가) '{id}'번 기사에 좋아요를 눌렀습니다.")
    try:
        news = News.objects.get(pk=id)
    except News.DoesNotExist:
        return Response({'error': '뉴스가 존재하지 않습니다.'}, status=404)

    try:
        # 좋아요 기록 생성
        activity, created = UserActivity.objects.get_or_create(
            user=user,
            news=news,
            action_type='like',
        )
        if not created:
            return Response({'message': '이미 좋아요를 눌렀습니다.'}, status=400)

        return Response({'message': '좋아요가 등록되었습니다.'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def is_news_liked(request, id):
    user = request.user
    
    if not user.is_authenticated:
        return Response({'is_liked': False}, status=200)

    is_liked = UserActivity.objects.filter(user=user, news=id, action_type='like').exists()
    return Response({'is_liked': is_liked}, status=200)

