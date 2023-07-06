from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import ArticleRSS


class BlogSitemap(Sitemap):
    chagefreq = "never"
    priority = 0.5

    def items(self):
        return (ArticleRSS.objects
        .filter(published_at__isnull=False)
        .order_by("-published_at")
        )

    def lastmod(self, obj: ArticleRSS):
        return obj.published_at
