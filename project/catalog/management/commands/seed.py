from django.core.management.base import BaseCommand

from catalog.models import Category, Product
from catalog.search_backend import ensure_index, index_product

CATEGORIES = [
    ("wireless", "Беспроводные"),
    ("wired", "Проводные"),
    ("tws", "TWS"),
    ("over-ear", "Полноразмерные"),
    ("in-ear", "Внутриканальные"),
]

PRODUCTS = [
    ("Sony WH-1000XM5", "Лучший шумодав с активным шумоподавлением", "32990", "wireless"),
    ("Apple AirPods Pro 2", "Премиум TWS с пространственным звуком", "21990", "tws"),
    ("Sennheiser HD 600", "Эталонные референсные проводные наушники", "28990", "wired"),
    ("JBL Tune 760NC", "Беспроводные с шумоподавлением, бюджетные", "8990", "wireless"),
    ("Bose QuietComfort Ultra", "Полноразмерные с лучшим шумодавом", "44990", "over-ear"),
    ("Marshall Major V", "Беспроводные с легендарным звучанием", "14990", "wireless"),
    ("Samsung Galaxy Buds 3 Pro", "TWS с продвинутым ANC", "18990", "tws"),
    ("AKG K712 Pro", "Открытые студийные наушники", "26990", "wired"),
]


class Command(BaseCommand):
    help = "Создаёт категории, продукты и индексирует их в Elasticsearch"

    def handle(self, *args, **options):
        ensure_index()
        category_map = {}
        for slug, name in CATEGORIES:
            obj, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
            category_map[slug] = obj

        for title, desc, price, slug in PRODUCTS:
            product, _ = Product.objects.get_or_create(
                title=title,
                defaults={
                    "description": desc,
                    "price": price,
                    "category": category_map[slug],
                },
            )
            index_product(product)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {Category.objects.count()} categories, "
                f"{Product.objects.count()} products (indexed in ES)"
            )
        )
