# accounts/serializers.py

from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from accounts.models import Profile, Category
from news.serializers import CategorySerializer

class CustomRegisterSerializer(RegisterSerializer):
    disliked_categories = serializers.JSONField(required=False)  # JSON 필드

    def save(self, request):
        user = super().save(request)
        disliked_categories = self.validated_data.get('disliked_categories', [])
        print("Disliked Categories:", disliked_categories)
        
        # Profile 생성 및 JSON 필드 설정
        profile, created = Profile.objects.get_or_create(user=user)
        profile.disliked_categories = disliked_categories  # JSON 데이터 저장
        profile.save()
        
        return user

class ProfileSerializer(serializers.ModelSerializer):
    preferred_categories = CategorySerializer(many=True)
    disliked_categories = CategorySerializer(many=True)

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'preferred_categories', 'disliked_categories']