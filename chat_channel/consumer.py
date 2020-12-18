import json
from urllib.parse import parse_qs

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class LiveScoreConsumer(WebsocketConsumer):
    def connect(self):
        data_dict = parse_qs(self.scope['query_string'].decode())
        consUsername = data_dict.get('consUsername', [None])[0]
        groupCode: str = data_dict.get('groupCode', ["None"])[0]
        groupCode = groupCode.replace(":", "    ")
        if True:
            self.username = consUsername
            self.room_name = groupCode
            self.room_group_name = f'chat_{self.room_name}'

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()
        # else:
        # self.room_name = "error"
        # self.room_group_name = f'chat_{self.room_name}'
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        # raise DenyConnection("Invalid User")

    def receive(self, text_data):
        print(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat.message",
             "text": "unknown request type", })

    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event['text']).encode('utf8').decode())

    def websocket_disconnect(self, message):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
