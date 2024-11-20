from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.category_name

class MediaCompany(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class News(models.Model):
    news_title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="news")
    media_company = models.ForeignKey(MediaCompany, on_delete=models.CASCADE, related_name="news")
    writer = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    summary = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField()
    sentiment_score = models.FloatField()

class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)
    news = models.ManyToManyField(News, related_name="tags")
