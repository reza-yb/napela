from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class ChatMessage(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    seen = models.BooleanField(default=False)
    text = models.TextField(null=True)
    message_date_time = models.DateTimeField()

    def __init__(self, owner, to, text, message_date_time, seen, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner
        self.to = to
        self.seen = seen
        self.text = text
        self.message_date_time = message_date_time
