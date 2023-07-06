from django.contrib import admin

from .models import ArticleRSS

@admin.register(ArticleRSS)
class ArticleAdmin(admin.ModelAdmin):
    list_display = "id", "title", "body", "published_at"
