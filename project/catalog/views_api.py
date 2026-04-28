from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["GET"])
def product_list(request):
    return JsonResponse({"page": "product_list", "items": []})


@csrf_exempt
@require_http_methods(["GET"])
def product_detail(request, product_id: int):
    return JsonResponse({"page": "product_detail", "id": product_id})


@csrf_exempt
@require_http_methods(["GET"])
def category_detail(request, slug: str):
    return JsonResponse({"page": "category_detail", "slug": slug})


@csrf_exempt
@require_http_methods(["GET"])
def profile(request):
    return JsonResponse({"page": "profile"})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def favorites(request):
    return JsonResponse({"page": "favorites", "method": request.method})
