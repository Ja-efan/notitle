from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse

# from .serializers import BoardListSerializer, BoardSerializer
# from .models import Board

from .serializers import NewsListSerializer, NewsSerializer 
from .models import News


# 게시글 생성(POST), 전체 게시글 조회(GET)
@api_view(['GET', 'POST'])
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
        