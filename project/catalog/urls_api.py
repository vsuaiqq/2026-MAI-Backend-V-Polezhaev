from django.urls import path

from . import views_api

app_name = "api"

urlpatterns = [
    path("search/", views_api.search, name="search"),
    path("products/", views_api.ProductListView.as_view(), name="product-list"),
    path("products/create/", views_api.ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/", views_api.ProductDetailView.as_view(), name="product-detail"),
    path("categories/", views_api.CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", views_api.CategoryDetailView.as_view(), name="category-detail"),
    path("profile/", views_api.profile, name="profile"),
    path("favorites/", views_api.favorites, name="favorites"),
]
