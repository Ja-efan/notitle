from rest_framework import serializers
from .models import News, Category, MediaCompany

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

class MediaCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaCompany
        fields = ( 'company_name', 'company_id')
        
        
class NewsListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name')  # 카테고리 이름 매핑
    media_company_name = serializers.CharField(source='media_company.company_name')  # 언론사 이름 매핑

    class Meta:
        model = News
        fields = ('article_id', 'keyword', 'category_name', 'title', 'content', 'summary', 'writer', 'published_date', 'url', 'media_company_name')


class NewsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name')  # 카테고리 이름 매핑
    media_company_name = serializers.CharField(source='media_company.company_name')  # 언론사 이름 매핑
    class Meta:
        model = News
        fields = '__all__'