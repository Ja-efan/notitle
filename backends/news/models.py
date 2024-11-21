from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.category_name

class MediaCompany(models.Model):
    # id 
    company_name = models.CharField(max_length=150, unique=True)
    company_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.comapany_name

class News(models.Model):
    article_id = models.CharField(primary_key=True, max_length=100)  # 기사 ID 추가
    title = models.CharField(max_length=255) # -> titme로 변경 하자 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="news")
    # 
    media_company = models.ForeignKey(MediaCompany, on_delete=models.CASCADE, related_name="news")
    writer = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    published_date = models.DateTimeField()
    # 크롤링 데이터 중복처리 -> url로 비교 or article_id로 비교 ? 
    # url 추가  
    url = models.URLField(max_length=500, null=True, blank=True)  # URL 필드 추가
    # article_id (네이버 뉴스 기사 자체 id): 2234983 (규칙이 있겟지만 알아보기 힘듬)

    # 추가적인 처리가 필요한 컬럼 : Spark -> OpenAI
    sentiment_score = models.FloatField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

    # keyword 필드
    # 1. 추가 할건가?
    # 2. 추가 한다면 어떻게 추출 할건가
    # 2-1. g 선생님
    # 2-2. 기사 자체 해시 태그 (있을 수도 없을 수도 -> 결국엔 g 선생님 도움 필요 )
    # 3. g 선생님으로 가자

class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)
    news = models.ManyToManyField(News, related_name="tags")
