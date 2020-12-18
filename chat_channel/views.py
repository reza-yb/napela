from django.shortcuts import render

# Create your views here.
from chat_channel.models import ChatMessage


def popup_chat_page(request):
    """View function for home page of site."""
    # TODO adding auth and getting prev messages after adding user table
    import datetime
    prev_messages = [ChatMessage(None, None, "hello", datetime.datetime.now(), False),
                     ChatMessage(None, None, "hi", datetime.datetime.now(), False),
                     ChatMessage(None, None, "how are you?", datetime.datetime.now(), False)]
    from django.core import serializers
    prev_messages_html = serializers.serialize("json", prev_messages)
    context = {'prev_messages': prev_messages, 'prev_messages_html': prev_messages_html}
    return render(request, 'chat_channel/popup_chat_page.html', context=context)

def chat_page_with_contact(request):
    """View function for home page of site."""
    # TODO adding auth and getting prev messages after adding user table
    import datetime
    prev_messages = [ChatMessage(None, None, "hello", datetime.datetime.now(), False),
                     ChatMessage(None, None, "hi", datetime.datetime.now(), False),
                     ChatMessage(None, None, "how are you?", datetime.datetime.now(), False)]
    from django.core import serializers
    prev_messages_html = serializers.serialize("json", prev_messages)
    context = {'prev_messages': prev_messages, 'prev_messages_html': prev_messages_html}
    return render(request, 'chat_channel/chat_page_with_contact.html', context=context)

