from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer  # NOTE: I have a lot to learn about other options here.
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # NOTE: So, is all data passed to receive just text? I guess I could
        # load it as JSON (catching exceptions) and pass it to a Form or
        # whatever. Should I avoid CPU-bound work? Does the ASGI server run
        # on an event loop? Probably.
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        # NOTE: I think I heard somewhere that you can direct messages back
        # through different sockets (or "channels"!). Perhaps there's an
        # argument you can give to `send` to control that, but since we don't
        # specify it sends on the same channel(?). So many questions!
        self.send(text_data=json.dumps({
            'message': message
        }))
