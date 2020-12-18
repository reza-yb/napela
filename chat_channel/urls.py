from django.urls import path

from chat_channel.views import popup_chat_page,chat_page_with_contact

app_name = 'home'
urlpatterns = [
    path('popup_chat_page/', popup_chat_page, name='popup_chat_page'),
    path('chat_page_with_contact/', chat_page_with_contact, name='chat_page_with_contact'),

]
