import datetime

from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.shortcuts import get_object_or_404


# TODO
def get_user_json(user_id):
    res = {"id": None, 'first_name': "", 'last_name': ""}
    try:
        user: User = get_object_or_404(User, pk=user_id)
        res['id'] = user.pk
        res['first_name'] = user.first_name
        res['last_name'] = user.last_name
    except:
        pass

    return res


class ChatMessage(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    seen = models.BooleanField(default=False)
    text = models.TextField(null=True)
    created_datetime = models.DateTimeField()

    def __init__(self, owner=None, to=None, text="", created_date_time=datetime.datetime.now(), seen=False,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner
        self.to = to
        self.seen = seen
        self.text = text
        self.created_datetime = created_date_time

    @classmethod
    def from_json(cls, data):
        owner_user_id = data['owner_user_id']
        to_user_id = data['to_user_id']
        seen = data.get('seen', False)
        text = data.get('text', "")
        created_date_time = data.get('created_date_time', datetime.datetime.now())
        """ creating object """
        chat = ChatMessage()
        chat.owner = get_object_or_404(User, pk=owner_user_id)
        chat.to = get_object_or_404(User, pk=to_user_id)
        chat.seen = seen
        chat.text = text
        chat.created_datetime = created_date_time
        return chat

    def to_json(self):
        owner_user_id = None
        try:
            owner_user_id = self.owner.id
        except:
            pass
        to_user_id = None
        try:
            to_user_id = self.to.id
        except:
            pass
        return {'owner': get_user_json(owner_user_id), 'to_user_id': get_user_json(to_user_id), 'seen': self.seen,
                'text': self.text,
                'created_datetime': str(self.created_datetime)}

class ChatContact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    contact_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contact_user")
    last_messages = models.ForeignKey(ChatMessage, on_delete=models.DO_NOTHING, related_name="last_message")