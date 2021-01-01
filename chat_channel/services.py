import json

from chat_channel.models import ChatMessage


class ConsumerService:
    @classmethod
    def change_group_and_room(cls, new_channel_room, consumer):
        from asgiref.sync import async_to_sync
        if consumer.room_name != new_channel_room and new_channel_room != "":
            async_to_sync(consumer.channel_layer.group_discard)(consumer.room_group_name, consumer.channel_name)
            consumer.room_name = new_channel_room
            consumer.room_group_name = f'chat_{consumer.room_name}'
            async_to_sync(consumer.channel_layer.group_add)(
                consumer.room_group_name,
                consumer.channel_name)

    @classmethod
    def new_chat_message(cls, socket_data):
        new_chat_message_data = socket_data.get('message_data', {})
        try:
            # TODO it raises an error while in authentication is not implemented
            chat_message = ChatMessage.from_json(new_chat_message_data)
            chat_message.save()
        except:
            pass
        return json.dumps(socket_data)

    @classmethod
    def unknown_message(cls, socket_data):
        return "unknown request type"