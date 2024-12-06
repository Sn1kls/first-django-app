import jwt
from django.conf import settings
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return User.objects.get(id=payload["user_id"])
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return None


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("Authorization", [None])[0]
        scope["user"] = None
        if token:
            scope["user"] = get_user_from_token(token)
        return self.inner(scope)


JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))
