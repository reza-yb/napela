import datetime
import json

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
            # TODO it raises an error while in authentication is not implemented
            contact_id = int(new_chat_message_data.get('contact_id', -1))
            contact = get_object_or_404(ChatContact, pk=contact_id)
            new_chat_message_data['to_user_id'] = contact.contact_user.pk

            ### setting time for message
            new_chat_message_data['created_date_time'] = str(datetime.datetime.now())

            chat_message = ChatMessage.from_json(new_chat_message_data)
            chat_message.save()
            """ updating chat contacts last messages """
            contact.last_message = chat_message
            contact.save()
            contact2 = ChatContact.objects.get(owner=contact.contact_user, contact_user=contact.owner)
            contact2.last_message = chat_message
            contact2.save()
        except Exception as e:
            print(e)
        socket_data['message_data'] = new_chat_message_data
        return json.dumps(socket_data)

    @classmethod
    def unknown_message(cls, socket_data):
        return json.dumps({'message_type': 'unknown request type', 'channel_room': "", 'message_data': {}})
