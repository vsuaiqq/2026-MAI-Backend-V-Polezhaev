from django.urls import path

from . import views_web

app_name = "web"

urlpatterns = [
    path("", views_web.home, name="home"),
    path("login/", views_web.login_page, name="login"),
    path("feed/", views_web.feed, name="feed"),
    path("categories/<slug:slug>/", views_web.category_detail, name="category"),
    path("products/<int:product_id>/", views_web.product_detail, name="product"),
    path("profile/", views_web.profile, name="profile"),
    path("favorites/", views_web.favorites, name="favorites"),
]
