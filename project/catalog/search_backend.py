import json

from django.conf import settings
from elasticsearch import Elasticsearch
import redis

_es = None
_redis = None


def get_es() -> Elasticsearch:
    global _es
    if _es is None:
        _es = Elasticsearch(settings.ES_URL)
    return _es


def get_redis() -> "redis.Redis":
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


def ensure_index() -> None:
    es = get_es()
    if not es.indices.exists(index=settings.ES_INDEX):
        es.indices.create(
            index=settings.ES_INDEX,
            mappings={
                "properties": {
                    "id": {"type": "long"},
                    "title": {"type": "text"},
                    "description": {"type": "text"},
                    "price": {"type": "keyword"},
                    "category": {"type": "keyword"},
                }
            },
        )


def index_product(product) -> None:
    ensure_index()
    get_es().index(
        index=settings.ES_INDEX,
        id=str(product.id),
        document={
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "price": str(product.price),
            "category": product.category.slug,
        },
        refresh="wait_for",
    )


def search_products(q: str) -> list:
    if not q:
        return []
    cache_key = f"search:{q}"
    r = get_redis()
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    es = get_es()
    result = es.search(
        index=settings.ES_INDEX,
        query={
            "multi_match": {
                "query": q,
                "fields": ["title^2", "description"],
            }
        },
    )
    hits = [h["_source"] for h in result["hits"]["hits"]]
    r.setex(cache_key, settings.SEARCH_CACHE_TTL, json.dumps(hits))
    return hits
