from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from catalog.factories import CategoryFactory, ProductFactory
from catalog.models import Product

User = get_user_model()


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("alice", "a@e.com", "pwd")
        self.client.force_login(self.user)
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

    def test_detail_404(self):
        response = self.client.get("/api/products/999999/")
        self.assertEqual(response.status_code, 404)

    @patch("catalog.views_api.publish_product")
    @patch("catalog.views_api.index_product")
    def test_create_indexes_in_es(self, mock_index, mock_publish):
        payload = {
            "title": "Sony WH-1000XM5",
            "description": "шумодав",
            "price": "32990.00",
            "category": self.category.slug,
        }
        response = self.client.post("/api/products/create/", payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(title="Sony WH-1000XM5").exists())
        mock_index.assert_called_once()
        mock_publish.assert_called_once()

    @patch("catalog.views_api.publish_product")
    @patch("catalog.views_api.index_product")
    def test_create_invalid(self, _mock_index, _mock_publish):
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


class SearchAPITests(TestCase):
    @patch("catalog.views_api.search_products")
    def test_search_calls_backend(self, mock_search):
        mock_search.return_value = [{"id": 1, "title": "Sony WH"}]
        response = self.client.get("/api/search/?q=Sony")
        self.assertEqual(response.status_code, 200)
        mock_search.assert_called_once_with("Sony")
        self.assertEqual(response.json()["count"], 1)

    @patch("catalog.views_api.search_products")
    def test_search_empty_q_no_call(self, mock_search):
        response = self.client.get("/api/search/?q=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)
        mock_search.assert_not_called()


class CategoryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("bob", "b@e.com", "pwd")
        self.client.force_login(self.user)
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


class AuthenticatedAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", "a@e.com", "pwd")
        self.client.force_login(self.user)

    def test_profile_returns_current_user(self):
        response = self.client.get("/api/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "alice")

    def test_profile_method_not_allowed(self):
        response = self.client.put("/api/profile/")
        self.assertEqual(response.status_code, 405)

    def test_favorites_get_empty(self):
        response = self.client.get("/api/favorites/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)

    def test_favorites_add(self):
        product = ProductFactory(category=CategoryFactory())
        response = self.client.post(f"/api/favorites/?product_id={product.id}")
        self.assertEqual(response.status_code, 201)
        self.assertIn(product, self.user.favorites.all())

    def test_favorites_add_missing_id(self):
        response = self.client.post("/api/favorites/")
        self.assertEqual(response.status_code, 400)

    def test_favorites_add_404(self):
        response = self.client.post("/api/favorites/?product_id=999999")
        self.assertEqual(response.status_code, 404)

    def test_favorites_lists_added(self):
        product = ProductFactory(category=CategoryFactory())
        self.user.favorites.add(product)
        response = self.client.get("/api/favorites/")
        self.assertEqual(response.json()["count"], 1)


class MiddlewareTests(TestCase):
    def test_anon_api_returns_401(self):
        response = self.client.get("/api/profile/")
        self.assertEqual(response.status_code, 401)

    def test_anon_web_redirects_to_login(self):
        response = self.client.get("/web/profile/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/web/login/", response.url)

    def test_anon_can_browse_public_endpoints(self):
        for url in [
            "/api/products/",
            "/api/categories/",
            "/web/",
            "/web/feed/",
            "/web/search/",
            "/web/products/live/",
        ]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, msg=url)

    def test_anon_create_blocked(self):
        response = self.client.post("/api/products/create/", {})
        self.assertEqual(response.status_code, 401)


class WebViewTests(TestCase):
    def test_home(self):
        response = self.client.get("/web/")
        self.assertEqual(response.status_code, 200)

    def test_login_page_has_google_button(self):
        response = self.client.get("/web/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "google-oauth2")

    def test_feed(self):
        response = self.client.get("/web/feed/")
        self.assertEqual(response.status_code, 200)

    def test_product_page(self):
        response = self.client.get("/web/products/1/")
        self.assertEqual(response.status_code, 200)

    def test_live_products_page(self):
        response = self.client.get("/web/products/live/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "public:products")
        self.assertContains(response, "centrifuge.js")

    @patch("catalog.views_web.search_products")
    def test_search_page_renders_results(self, mock_search):
        mock_search.return_value = [
            {"id": 1, "title": "Sony WH", "description": "x", "price": "100", "category": "wireless"},
        ]
        response = self.client.get("/web/search/?q=Sony")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sony WH")
        mock_search.assert_called_once_with("Sony")

    def test_search_page_empty(self):
        response = self.client.get("/web/search/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Найдено:")

    def test_method_not_allowed(self):
        response = self.client.put("/web/")
        self.assertEqual(response.status_code, 405)
