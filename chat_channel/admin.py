from django.contrib import admin

# Register your models here.
from chat_channel.models import ChatMessage, ChatContact

admin.site.register(ChatMessage)
admin.site.register(ChatContact)
