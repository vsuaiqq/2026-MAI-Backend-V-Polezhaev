from unittest.mock import patch

from django.test import TestCase

from catalog.factories import CategoryFactory, ProductFactory


class SearchMockTests(TestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.product = ProductFactory(title="hello", category=self.category)

    @patch("catalog.views_api.ProductSerializer")
    def test_search_uses_serializer(self, MockSerializer):
        MockSerializer.return_value.data = [{"id": 1, "title": "mocked"}]
        response = self.client.get("/api/search/?q=hello")
        self.assertEqual(response.status_code, 200)
        MockSerializer.assert_called_once()
        self.assertEqual(response.json()["results"], [{"id": 1, "title": "mocked"}])

    @patch("catalog.views_api.Product.objects")
    def test_search_calls_filter(self, mock_objects):
        mock_objects.select_related.return_value.filter.return_value.count.return_value = 0
        mock_objects.select_related.return_value.filter.return_value.__iter__ = lambda s: iter([])
        response = self.client.get("/api/search/?q=hello")
        self.assertEqual(response.status_code, 200)
        mock_objects.select_related.assert_called_once_with("category")
