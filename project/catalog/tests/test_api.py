from django.test import TestCase
from rest_framework.test import APIClient

from catalog.factories import CategoryFactory, ProductFactory
from catalog.models import Product


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = CategoryFactory()
        self.products = ProductFactory.create_batch(3, category=self.category)

    def test_list(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_detail(self):
        product = self.products[0]
        response = self.client.get(f"/api/products/{product.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], product.id)
        self.assertEqual(response.json()["title"], product.title)

    def test_detail_404(self):
        response = self.client.get("/api/products/999999/")
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        payload = {
            "title": "Sony WH-1000XM5",
            "description": "шумодав",
            "price": "32990.00",
            "category": self.category.slug,
        }
        response = self.client.post("/api/products/create/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(title="Sony WH-1000XM5").exists())

    def test_create_invalid(self):
        response = self.client.post("/api/products/create/", {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update(self):
        product = self.products[0]
        response = self.client.patch(
            f"/api/products/{product.id}/",
            {"title": "Updated"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        product.refresh_from_db()
        self.assertEqual(product.title, "Updated")

    def test_delete(self):
        product = self.products[0]
        response = self.client.delete(f"/api/products/{product.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(pk=product.id).exists())

    def test_search_in_title(self):
        ProductFactory(title="Беспроводные Sony", description="x", category=self.category)
        response = self.client.get("/api/search/?q=Sony")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.json()["count"], 1)

    def test_search_in_description(self):
        ProductFactory(title="x", description="лучший Sony в городе", category=self.category)
        response = self.client.get("/api/search/?q=sony")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.json()["count"], 1)

    def test_search_empty(self):
        response = self.client.get("/api/search/?q=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)


class CategoryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.categories = CategoryFactory.create_batch(2)

    def test_list(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_detail(self):
        category = self.categories[0]
        response = self.client.get(f"/api/categories/{category.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["slug"], category.slug)

    def test_update(self):
        category = self.categories[0]
        response = self.client.patch(
            f"/api/categories/{category.id}/",
            {"name": "Новое имя"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        category.refresh_from_db()
        self.assertEqual(category.name, "Новое имя")

    def test_delete(self):
        category = self.categories[0]
        response = self.client.delete(f"/api/categories/{category.id}/")
        self.assertEqual(response.status_code, 204)


class StubViewTests(TestCase):
    def test_profile(self):
        response = self.client.get("/api/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["page"], "profile")

    def test_profile_method_not_allowed(self):
        response = self.client.put("/api/profile/")
        self.assertEqual(response.status_code, 405)

    def test_favorites_get(self):
        response = self.client.get("/api/favorites/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["method"], "GET")

    def test_favorites_post(self):
        response = self.client.post("/api/favorites/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["method"], "POST")


class WebViewTests(TestCase):
    def test_home(self):
        response = self.client.get("/web/")
        self.assertEqual(response.status_code, 200)

    def test_feed(self):
        response = self.client.get("/web/feed/")
        self.assertEqual(response.status_code, 200)

    def test_product_page(self):
        response = self.client.get("/web/products/1/")
        self.assertEqual(response.status_code, 200)

    def test_method_not_allowed(self):
        response = self.client.put("/web/")
        self.assertEqual(response.status_code, 405)
