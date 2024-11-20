from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, UserActivity

# User 모델을 기본 UserAdmin으로 관리
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(UserActivity)
