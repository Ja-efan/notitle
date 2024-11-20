from django.db import models
from accounts.models import User
from news.models import News

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations")
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="recommended_to_users")
    score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class KeywordOfYesterday(models.Model):
    date = models.DateField(unique=True)
    keyword_of_date = models.JSONField()

    def __str__(self):
        return f"Keywords for {self.date}"
