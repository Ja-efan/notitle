from django.contrib import admin
from .models import News, Category, MediaCompany, Tag

# admin.site.register(News)
# admin.site.register(Category)
# admin.site.register(MediaCompany)
# admin.site.register(Tag)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'media_company', 'writer', 'published_date', 'url', 'article_id')  # article_id 추가
