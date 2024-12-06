import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from users.models import Notification
from users.serializers import NotificationSerializer


logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"WebSocket connect request from {self.scope['user']}")
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            logger.warning("Unauthenticated WebSocket connection attempt")
            await self.close()
            return

        self.room_group_name = f"user_{self.user.id}_notifications"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnect from {self.scope['user']}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        logger.info(f"Message received on WebSocket: {text_data}")

    async def send_notification(self, event):
        message = event["message"]
        logger.info(f"Sending notification: {message}")
        await self.send(text_data=json.dumps({
            "message": message
        }))