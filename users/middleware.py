import logging
from urllib.parse import parse_qs

import jwt
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload["user_id"])
        logger.info(f"User authenticated: {user.email}")
        return user
    except jwt.ExpiredSignatureError:
        logger.error("Token expired")
    except jwt.DecodeError:
        logger.error("Invalid token")
    except User.DoesNotExist:
        logger.error("User not found")
    return AnonymousUser()


logger = logging.getLogger(__name__)


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("Authorization", [None])[0]
        logger.info(f"Token received: {token}")

        if token and token.startswith("Bearer "):
            token = token.split("Bearer ")[1]
        else:
            logger.error("Invalid token format or missing Bearer prefix")
            token = None

        if token:
            scope["user"] = await get_user_from_token(token)
            if isinstance(scope["user"], AnonymousUser):
                logger.error("Authentication failed: AnonymousUser returned")
            else:
                logger.info(f"Authenticated user: {scope['user'].email}")
        else:
            logger.warning("No valid token provided, defaulting to AnonymousUser")
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)


JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))
