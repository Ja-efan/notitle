from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg, F
from wordcloud import WordCloud
from io import BytesIO
import base64

from .serializers import NewsListSerializer, NewsSerializer, CategorySerializer
from .models import News, Category

FONT_PATH = "/usr/share/fonts/truetype/nanum/NanumSquareRoundB.ttf"

# 게시글 생성(POST), 전체 게시글 조회(GET)
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def news_list(request):
    if request.method == 'POST':
        # 사용자로부터 받은 입력을 포장
        serializer = NewsListSerializer(data=request.data)
        # 포장된 데이터가 모두 정상적일 때(유효성 검증을 통과했을 때),
        if serializer.is_valid():
            # 사용자 입력이 아닌 다른 필드들을 함께 저장하도록 코드를 구성
            # serializer.save(writer=request.user)
            return Response(serializer.data)
    else:
        # 카테고리 필터링 
        category = request.query_params.get('category', None)
        print(f"사용자 선택 카테고리: {category}")
        if category is None or category == '전체':
            news = News.objects.all().order_by('-pk')
        else:
            news = News.objects.filter(category__category_name=category)

        serializer = NewsListSerializer(news, many=True)
        # print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def news_detail(request, id):
    print(f"사용자 선택 뉴스 ID: {id}")
    try :
        news = News.objects.get(article_id=id)  # 
        serializer = NewsSerializer(news)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except News.DoesNotExist:
        return Response({'error': "News not found"}, status=status.HTTP_404_NOT_FOUND)
        


@api_view(['GET'])
def news_analysis(request):
    try:
        # 총 뉴스 기사 수
        total_articles = News.objects.count()

        # 긍정 및 부정 감성 점수 분리
        positive_sentiment_count = News.objects.filter(sentiment_score__gt=0).count()
        negative_sentiment_count = News.objects.filter(sentiment_score__lt=0).count()

        # 감성 점수 평균
        avg_sentiment = News.objects.aggregate(avg_sentiment=Avg("sentiment_score"))

        # 카테고리별 기사 분포
        category_distribution = News.objects.values("category__category_name").annotate(count=Count("article_id"))

        # 상위 5명의 기자
        top_authors = News.objects.values("writer").annotate(count=Count("article_id")).order_by("-count")[:5]

        # 분석 데이터 구성
        analysis_data = {
            "total_articles": total_articles,
            "avg_sentiment": avg_sentiment.get("avg_sentiment"),
            "sentiment_distribution": {
                "positive": News.objects.filter(sentiment_score=1).count(),
                "neutral": News.objects.filter(sentiment_score=0).count(),
                "negative": News.objects.filter(sentiment_score=-1).count(),
            },
            "category_distribution": category_distribution,
            "top_authors": top_authors,
        }

        # print(f"01. analysis_data: {analysis_data}")
        # 워드 클라우드를 위한 키워드 데이터 
        keywords = News.objects.values_list('keyword', flat=True)
        combined_keywords = " ".join(keywords)

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            font_path=FONT_PATH
        ).generate(combined_keywords)

        # 워드 클라우드 이미지를 Base64로 변환
        buffer = BytesIO()
        wordcloud.to_image().save(buffer, format='PNG')
        buffer.seek(0)
        wordcloud_base64 = base64.b64encode(buffer.getvalue()).decode()

        # 워드 클라우드 데이터를 응답에 포함 
        analysis_data['wordcloud'] = wordcloud_base64
        # print(f"02. analysis_data: {analysis_data}")

        # print(analysis_data)
        return Response(analysis_data, status=200)
    except Exception as e:
        print(f"Error occured: {str(e)}")
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def liked_news(request):
    user = request.user
    # 좋아요 누른 뉴스 필터링
    liked_news = News.objects.filter(user_activities__user=user, user_activities__action_type='like')
    serializer = NewsSerializer(liked_news, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    """
    모든 카테고리 목록을 반환하는 API 엔드포인트
    """
    try:
        categories = Category.objects.all()  # 모든 카테고리 가져오기
        # print(categories)
        serializer = CategorySerializer(categories, many=True)  # 카테고리 시리얼라이징
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
