from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.category_name

class MediaCompany(models.Model):
    company_id = models.IntegerField(primary_key=True, unique=True)
    company_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.comapany_name

class News(models.Model):
    article_id = models.CharField(primary_key=True, max_length=100)  # 기사 ID 추가
    title = models.CharField(max_length=255) # -> titme로 변경 하자 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="news")
    # 
    media_company = models.ForeignKey(MediaCompany, on_delete=models.CASCADE, related_name="news")
    # 외래키가 기본 아이로 되어있어서 3자리 이상 못잡는거같은데
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
    keyword = models.TextField(null=True, blank=True)

class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)
    news = models.ManyToManyField(News, related_name="tags")
