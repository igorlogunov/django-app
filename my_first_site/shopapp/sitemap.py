from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product


class ShopSitemap(Sitemap):
    chagefreq = "never"
    priority = 0.5

    def items(self):
        return (Product.objects.order_by("-created_at"))

    def lastmod(self, obj: Product):
        return obj.created_at
