import json

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from chat_channel.models import ChatMessage, ChatContact


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
            ### setting time for message
            chat_message = ChatMessage.from_json(new_chat_message_data)
            chat_message.save()
            socket_data['message_data'] = chat_message.to_json()

            """ updating chat contacts last messages """
            contact = ChatContact.objects.get(owner=chat_message.owner, contact_user=chat_message.to)
            contact.last_message = chat_message
            contact.save()
            contact2 = ChatContact.objects.get(owner=chat_message.to, contact_user=chat_message.owner)
            contact2.last_message = chat_message
            contact2.save()
        except Exception as e:
            print(e)
        return json.dumps(socket_data)

    @classmethod
    def unknown_message(cls, socket_data):
        return json.dumps({'message_type': 'unknown request type', 'channel_room': "", 'message_data': {}})

    @classmethod
    def set_channel(cls, socket_data):
        return json.dumps({'message_type': 'set_channel', 'channel_room': "", 'message_data': {}})
