from rest_framework import serializers
from .models import News, Category

# 게시글
# 1. 전체 게시글 조회
# 2. 게시글 생성
#   - 사용자 입력: 제목, 내용
#   - 자동 입력: 유저 정보
# ModelSerializer: DB 에 정의된 필드 안에서만 포장을 하고 싶을 때
# Serializer: DB 에 정의된 필드 말고도 포장을 하고 싶을 때

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name')

class NewsListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = News
        fields = ('id', 'category', 'news_title', 'content', 'writer', 'published_date',)

# 3. 상세 게시글 (조회, 수정)
#   - 모든 필드 다 조회
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'