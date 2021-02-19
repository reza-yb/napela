from channels.routing import URLRouter
from django.urls import path

from chat_channel.consumer import LiveScoreConsumer

websockets = URLRouter([
    path("ws/chat", LiveScoreConsumer, name="chat_messages", ),
])
