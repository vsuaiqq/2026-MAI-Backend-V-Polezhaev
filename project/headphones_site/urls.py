from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("web/", include("catalog.urls_web", namespace="web")),
    path("api/", include("catalog.urls_api", namespace="api")),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("accounts/", include("django.contrib.auth.urls")),
]
