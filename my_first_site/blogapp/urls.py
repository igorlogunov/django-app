from django.urls import path, include

from .views import (
    ArticlesListView,
    ArticlesRSSListView,
    ArticleRSSDetailView,
    LatestArticlesFeed,
)

app_name = "blogapp"

urlpatterns = [
    path("articles/", ArticlesListView.as_view(), name="articles_list"),
    path("articles_rss/", ArticlesRSSListView.as_view(), name="articles"),
    path("articles_rss/<int:pk>/", ArticleRSSDetailView.as_view(), name="article"),
    path("articles_rss/latest/feed/", LatestArticlesFeed(), name="articles-feed")
]