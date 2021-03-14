from django.urls import path

from chat_channel.views import chat_page_with_contact, get_prev_messages

app_name = 'home'
urlpatterns = [
    path('my_chatroom/<int:to_user_id>/', chat_page_with_contact, name='chat_page_with_contact'),
    path('prev_messages/<to_contact_id>/', get_prev_messages, name='get_pre_messages')

]
