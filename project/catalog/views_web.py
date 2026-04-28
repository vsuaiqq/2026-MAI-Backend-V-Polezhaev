from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .search_backend import search_products


@csrf_exempt
@require_http_methods(["GET"])
def home(request):
    return render(request, "catalog/home.html")


@csrf_exempt
@require_http_methods(["GET"])
def search_page(request):
    q = (request.GET.get("q") or "").strip()
    results = search_products(q) if q else []
    return render(
        request,
        "catalog/search.html",
        {"q": q, "count": len(results), "results": results},
    )


@csrf_exempt
@require_http_methods(["GET"])
def login_page(request):
    return render(request, "catalog/login.html")


@csrf_exempt
@require_http_methods(["GET"])
def feed(request):
    return render(request, "catalog/feed.html")


@csrf_exempt
@require_http_methods(["GET"])
def category_detail(request, slug: str):
    return render(request, "catalog/category.html", {"slug": slug})


@csrf_exempt
@require_http_methods(["GET"])
def product_detail(request, product_id: int):
    return render(request, "catalog/product.html", {"product_id": product_id})


@csrf_exempt
@require_http_methods(["GET"])
def profile(request):
    return render(request, "catalog/profile.html")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def favorites(request):
    products = request.user.favorites.all()
    return render(request, "catalog/favorites.html", {"products": products})
