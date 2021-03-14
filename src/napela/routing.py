from channels.routing import ProtocolTypeRouter

from chat_channel.routing import websockets

application = ProtocolTypeRouter({
    "websocket": websockets,
})
