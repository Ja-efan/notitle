from django.db import models
from news.models import Category, MediaCompany
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)  # 이메일을 고유 필드로 사용
    created_at = models.DateTimeField(auto_now_add=True)  # 계정 생성일

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    date_of_birth = models.DateField(null=True, blank=True)
    preferred_categories = models.ManyToManyField(Category, related_name="preferred_by_users")
    disliked_categories = models.JSONField(default=list, blank=True)  # JSON 형식으로 비선호 카테고리 저장
    preferred_media_companies = models.ManyToManyField(MediaCompany, related_name="preferred_by_users")

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    news = models.ForeignKey("news.News", on_delete=models.CASCADE, related_name="user_activities", to_field="article_id")
    action_type = models.CharField(max_length=20, choices=[
        ("view", "View"),
        ("like", "Like"),
        ("share", "Share")
    ])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('news', 'user', 'action_type')  # 중복 방지

        
