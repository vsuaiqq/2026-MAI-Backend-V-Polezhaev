from unittest.mock import MagicMock, patch

from django.test import TestCase

from catalog.factories import CategoryFactory, ProductFactory


class SearchBackendMockTests(TestCase):
    @patch("catalog.views_api.search_products")
    def test_view_uses_search_products(self, mock_search):
        mock_search.return_value = [{"id": 1, "title": "mocked"}]
        response = self.client.get("/api/search/?q=hello")
        self.assertEqual(response.status_code, 200)
        mock_search.assert_called_once_with("hello")
        self.assertEqual(response.json()["results"], [{"id": 1, "title": "mocked"}])

    @patch("catalog.search_backend.get_es")
    @patch("catalog.search_backend.get_redis")
    def test_search_backend_caches_in_redis(self, mock_redis, mock_es):
        from catalog.search_backend import search_products

        r = MagicMock()
        r.get.return_value = None
        mock_redis.return_value = r

        es = MagicMock()
        es.search.return_value = {"hits": {"hits": [{"_source": {"id": 1, "title": "x"}}]}}
        mock_es.return_value = es

        result = search_products("foo")
        self.assertEqual(result, [{"id": 1, "title": "x"}])
        es.search.assert_called_once()
        r.setex.assert_called_once()


class IndexProductMockTests(TestCase):
    def setUp(self):
        self.category = CategoryFactory()

    @patch("catalog.search_backend.get_es")
    def test_index_product_calls_es_index(self, mock_es):
        from catalog.search_backend import index_product

        es = MagicMock()
        es.indices.exists.return_value = True
        mock_es.return_value = es

        product = ProductFactory(category=self.category, title="Sony")
        index_product(product)

        es.index.assert_called_once()
        kwargs = es.index.call_args.kwargs
        self.assertEqual(kwargs["document"]["title"], "Sony")
        self.assertEqual(kwargs["document"]["category"], self.category.slug)
