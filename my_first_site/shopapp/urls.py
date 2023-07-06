from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailsView,
    ProductListView,
    OrdersListView,
    OrdersDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    ProductDataExportView,
    OrderDataExportView,
    ProductViewSet,
    OrderViewSet,
    LatestProductsFeed,
    UserOrdersListView,
    UserOrdersDataExportView,
)

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    # path("", cache_page(60 * 3)(ShopIndexView.as_view()), name="index"),
    path("", ShopIndexView.as_view(), name="index"),
    path("api/", include(routers.urls)),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/export/", ProductDataExportView.as_view(), name="products_export"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/latest/feed/", LatestProductsFeed(), name="product_feed"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/export/", OrderDataExportView.as_view(), name="orders_export"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/", OrdersDetailView.as_view(), name="order_details"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name="users_orders"),
    path("users/<int:user_id>/orders/export/", UserOrdersDataExportView.as_view(), name="users_orders_export"),

]