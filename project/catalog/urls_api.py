from django.urls import path

from . import views_api

app_name = "api"

urlpatterns = [
    path("products/", views_api.product_list, name="product-list"),
    path("products/<int:product_id>/", views_api.product_detail, name="product-detail"),
    path("categories/<slug:slug>/", views_api.category_detail, name="category"),
    path("profile/", views_api.profile, name="profile"),
    path("favorites/", views_api.favorites, name="favorites"),
]
