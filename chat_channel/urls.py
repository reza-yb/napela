from django.urls import path

from chat_channel.views import chat_page_with_contact, get_prev_messages

app_name = 'home'
urlpatterns = [
    path('chat_page_with_contact/<int:to_user_id>/', chat_page_with_contact, name='chat_page_with_contact'),
    path('prev_messages/<owner_user_id>/<to_user_id>/', get_prev_messages, name='get_pre_messages')

]
