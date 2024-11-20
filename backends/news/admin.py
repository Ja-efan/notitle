from django.contrib import admin
from .models import News, Category, MediaCompany, Tag

admin.site.register(News)
admin.site.register(Category)
admin.site.register(MediaCompany)
admin.site.register(Tag)
