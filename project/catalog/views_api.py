from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import generics

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@csrf_exempt
@require_http_methods(["GET"])
def search(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return JsonResponse({"q": q, "count": 0, "results": []})
    qs = Product.objects.select_related("category").filter(
        Q(title__icontains=q) | Q(description__icontains=q)
    )
    serializer = ProductSerializer(qs, many=True)
    return JsonResponse({"q": q, "count": qs.count(), "results": serializer.data})


@csrf_exempt
@require_http_methods(["GET"])
def profile(request):
    user = request.user
    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })


@csrf_exempt
@require_http_methods(["GET", "POST"])
def favorites(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id") or request.GET.get("product_id")
        if not product_id:
            return JsonResponse({"detail": "product_id required"}, status=400)
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"detail": "Не найдено"}, status=404)
        request.user.favorites.add(product)
        return JsonResponse({"detail": "added", "product_id": product.id}, status=201)

    serializer = ProductSerializer(request.user.favorites.all(), many=True)
    return JsonResponse({"count": len(serializer.data), "results": list(serializer.data)})
