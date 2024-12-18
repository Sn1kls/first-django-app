import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        # Прив'язуємо підключення конкретно до користувача
        self.channel_name_for_user = f"user_{self.user.id}_channel"
        await self.accept()

        logger.info(f"User {self.user.id} connected to WebSocket on channel {self.channel_name}")

    async def disconnect(self, close_code):
        logger.info(f"User {self.user.id} disconnected from WebSocket.")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            logger.info(f"Received data: {data}")
            action = data.get("action")

            if action == "subscribe":
                await self.send(text_data=json.dumps({"status": "subscribed", "user": str(self.user.id)}))
            else:
                await self.send(text_data=json.dumps({"error": "Invalid action or missing parameters"}))

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON format"}))

    async def send_notification(self, event):
        """
        Метод для відправки повідомлення конкретному користувачу.
        """
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
