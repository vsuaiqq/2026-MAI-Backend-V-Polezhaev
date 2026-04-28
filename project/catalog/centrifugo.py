import json
import time
import urllib.error
import urllib.request

import jwt
from django.conf import settings

CHANNEL = "public:products"


def build_connection_token(user):
    if not settings.CENTRIFUGO_SECRET:
        return ""
    if user.is_authenticated:
        sub = str(user.id)
    else:
        sub = "guest"
    payload = {
        "sub": sub,
        "exp": int(time.time()) + 3600,
    }
    return jwt.encode(payload, settings.CENTRIFUGO_SECRET, algorithm="HS256")


def publish_product(product_dict):
    if not settings.CENTRIFUGO_API_KEY or not settings.CENTRIFUGO_PUBLISH_URL:
        return
    body = json.dumps({"channel": CHANNEL, "data": {"product": product_dict}}).encode()
    req = urllib.request.Request(
        settings.CENTRIFUGO_PUBLISH_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": settings.CENTRIFUGO_API_KEY,
        },
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except urllib.error.URLError:
        pass
