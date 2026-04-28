import factory

from .models import Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    slug = factory.Sequence(lambda n: f"cat-{n}")
    name = factory.Faker("word")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    category = factory.SubFactory(CategoryFactory)
