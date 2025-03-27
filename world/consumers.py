import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Region

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.region_id = self.scope['url_route']['kwargs']['region_id']
        self.room_group_name = f'chat_{self.region_id}'

        # Check if the user is authenticated
        if self.scope.get("user").is_anonymous:
            await self.close()  # Reject unauthenticated connections
        else:
            # Add the user to the corresponding chat group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the chat group when disconnected
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Handle receiving a new chat message
        user = self.scope["user"]
        if user.is_anonymous:
            return

        data = json.loads(text_data)
        message = data['message']

        # Use sync_to_async to access the database in an async context
        region = await self.get_region(self.region_id)

        # Assuming you have a `ChatMessage` model to save the messages
        chat_message = await self.create_chat_message(region, user, message)

        # Send the message to the WebSocket group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username,
                'avatar': user.avatar.url if user.avatar else '/static/default-avatar.png',
                'timestamp': chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

    async def chat_message(self, event):
        # Send the received message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'avatar': event['avatar'],
            'timestamp': event['timestamp']
        }))

    # Wrap database calls in sync_to_async
    @database_sync_to_async
    def get_region(self, region_id):
        return Region.objects.get(id=region_id)

    @database_sync_to_async
    def create_chat_message(self, region, user, message):
        from .models import ChatMessage
        return ChatMessage.objects.create(region=region, user=user, message=message)