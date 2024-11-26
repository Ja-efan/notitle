from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import UserActivity
from news.models import News
from .serializers import ProfileSerializer

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
        return Response({'error': '뉴스가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # 좋아요 기록 생성
        activity, created = UserActivity.objects.get_or_create(
            user=user,
            news=news,
            action_type='like',
        )
        if not created:
            return Response({'message': '이미 좋아요를 눌렀습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': '좋아요가 등록되었습니다.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def is_news_liked(request, id):
    user = request.user
    
    if not user.is_authenticated:
        return Response({'is_liked': False}, status=status.HTTP_200_OK)

    is_liked = UserActivity.objects.filter(user=user, news=id, action_type='like').exists()
    return Response({'is_liked': is_liked}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_news_like(request, id):
    # 뉴스 기사 가져오기 
    news = get_object_or_404(News, article_id=id)

    # 좋아요 개수 카운트 
    like_count = UserActivity.objects.filter(news=news, action_type='like').count()

    return Response({'like_count': like_count}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 로그인된 사용자만 접근 가능
def user_profile(request):
    print(request.user)
    user = request.user  # 현재 요청한 사용자
    if not hasattr(user, 'profile'):  # 사용자가 프로필을 가지지 않는 경우
        return Response({"detail": "Profile not found."}, status=404)
    
    profile = user.profile
    serializer = ProfileSerializer(profile)
    print(f"{user}의 profile: {serializer }")
    return Response(serializer.data, status=200)
