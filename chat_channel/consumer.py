import json
from urllib.parse import parse_qs

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat_channel.services import ConsumerService


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
        socket_data = json.loads(text_data)
        message_type = socket_data.get('message_type', "unknown")
        """ changing channel if necessary """
        message_channel = socket_data.get('channel_room', "unknown")
        ConsumerService.change_group_and_room(message_channel, self)
        """"""""""""""""""""""""""""""""
        """ processing data message  """
        """"""""""""""""""""""""""""""""
        response_message_json = {}
        if message_type == "new_chat_message":
            response_message_json = ConsumerService.new_chat_message(socket_data)
        elif message_type == "set_channel":
            pass
        else:
            response_message_json = ConsumerService.unknown_message(socket_data)

        """ sending response message """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message",
                                   "text": response_message_json, })

    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event['text']).encode('utf8').decode())

    def websocket_disconnect(self, message):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)