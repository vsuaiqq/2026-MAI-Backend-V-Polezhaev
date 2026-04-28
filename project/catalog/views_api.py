import json

from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Category, Product


def _product_to_dict(p: Product) -> dict:
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "price": str(p.price),
        "category": p.category.slug,
    }


def _parse_body(request):
    if request.content_type == "application/json":
        try:
            return json.loads(request.body or b"{}")
        except json.JSONDecodeError:
            return None
    return request.POST.dict()


@csrf_exempt
@require_http_methods(["GET"])
def product_list(request):
    items = [_product_to_dict(p) for p in Product.objects.select_related("category")]
    return JsonResponse({"count": len(items), "results": items})


@csrf_exempt
@require_http_methods(["POST"])
def product_create(request):
    data = _parse_body(request)
    if data is None:
        return JsonResponse({"detail": "Невалидный JSON"}, status=400)

    title = (data.get("title") or "").strip()
    if not title:
        return JsonResponse({"detail": "title обязателен"}, status=400)

    category_slug = data.get("category")
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return JsonResponse({"detail": "Категория не найдена"}, status=400)

    try:
        product = Product.objects.create(
            title=title,
            description=data.get("description", ""),
            price=data.get("price", 0),
            category=category,
        )
    except (IntegrityError, ValueError) as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    return JsonResponse(_product_to_dict(product), status=201)


@csrf_exempt
@require_http_methods(["GET"])
def product_detail(request, product_id: int):
    try:
        product = Product.objects.select_related("category").get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"detail": "Не найдено"}, status=404)
    return JsonResponse(_product_to_dict(product))


@csrf_exempt
@require_http_methods(["GET"])
def category_detail(request, slug: str):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return JsonResponse({"detail": "Не найдено"}, status=404)
    items = [_product_to_dict(p) for p in category.products.select_related("category")]
    return JsonResponse({"slug": category.slug, "name": category.name, "products": items})


@csrf_exempt
@require_http_methods(["GET"])
def search(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return JsonResponse({"q": q, "count": 0, "results": []})
    qs = Product.objects.select_related("category").filter(
        Q(title__icontains=q) | Q(description__icontains=q)
    )
    items = [_product_to_dict(p) for p in qs]
    return JsonResponse({"q": q, "count": len(items), "results": items})


@csrf_exempt
@require_http_methods(["GET"])
def profile(request):
    return JsonResponse({"page": "profile"})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def favorites(request):
    return JsonResponse({"page": "favorites", "method": request.method})
