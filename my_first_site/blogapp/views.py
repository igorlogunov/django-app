from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy

from .models import Article, ArticleRSS


class ArticlesListView(ListView):
    template_name = 'blogapp/article_list.html'
    context_object_name = "articles"
    queryset = Article.objects.select_related("author").select_related("category").prefetch_related("tags").defer("content")

class ArticlesRSSListView(ListView):
    queryset = (
        ArticleRSS.objects
        .filter(published_at__isnull=False)
        .order_by("-published_at")
    )

class ArticleRSSDetailView(DetailView):
    model = ArticleRSS

class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes and addition blog articles"
    link = reverse_lazy("blogapp:articles")

    def items(self):
        return (
            ArticleRSS.objects
            .filter(published_at__isnull=False)
            .order_by("-published_at")[:5]
        )

    def item_title(self, item: ArticleRSS):
        return item.title

    def item_description(self, item: ArticleRSS):
        return item.body[:200]

    def item_link(self, item: ArticleRSS):
        return reverse("blogapp:article", kwargs={"pk": item.pk})