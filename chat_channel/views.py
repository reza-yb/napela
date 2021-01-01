from django.contrib.auth.models import User
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from chat_channel.models import ChatMessage, get_user_json


@csrf_exempt
def get_prev_messages(request, owner_user_id, to_user_id):
    """View function for home page of site."""
    # TODO adding auth and getting prev messages after adding user table
    import datetime
    import json
    from django.http.response import HttpResponse
    prev_messages = [ChatMessage(None, None, "hello", datetime.datetime.now(), False).to_json(),
                     ChatMessage(None, None, "hi", datetime.datetime.now(), False).to_json(),
                     ChatMessage(None, None, "how are you?", datetime.datetime.now(), False).to_json()]
    contact_user = get_user_json(to_user_id);
    contact_user['first_name'] = "aa"
    contact_user['last_name'] = "aa"
    return HttpResponse(json.dumps({'prev_messages': prev_messages, 'contact_info': contact_user}))


def popup_chat_page(request):
    """View function for home page of site."""
    # TODO adding auth and getting prev messages after adding user table
    u1 = User()
    u1.first_name = "aa"
    u1.last_name = "aa"
    u2 = User()
    u2.first_name = "bb"
    u2.last_name = "bb"
    context = {'contacts': [u1, u2]}
    return render(request, 'chat_channel/popup_chat_page.html', context=context)


def chat_page_with_contact(request):
    """View function for home page of site."""
    # TODO adding auth and getting prev messages after adding user table

    u1 = User()
    u1.first_name = "aa"
    u1.last_name = "aa"
    u2 = User()
    u2.first_name = "bb"
    u2.last_name = "bb"
    context = {'contacts': [u1, u2]}
    return render(request, 'chat_channel/chat_page_with_contact.html', context=context)