from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from chat_channel.models import ChatMessage, get_user_json, ChatContact


@csrf_exempt
@login_required
def get_prev_messages(request, to_contact_id):
    """View function for home page of site."""
    # TODO adding auth and getting prev messages after adding user table

    contact = get_object_or_404(ChatContact, pk=to_contact_id)
    import json
    from django.http.response import HttpResponse
    prev_messages = ChatMessage.objects.filter(
        Q(owner=request.user, to=contact.contact_user) | Q(to=request.user, owner=contact.contact_user))
    contact_user = get_user_json(contact.contact_user)
    return HttpResponse(json.dumps({'prev_messages': list(prev_messages), 'contact_info': contact_user}))


# def popup_chat_page(request):
#     """View function for home page of site."""
#     # TODO adding auth and getting prev messages after adding user table
#     u1 = User()
#     u1.first_name = "aa"
#     u1.last_name = "aa"
#     u2 = User()
#     u2.first_name = "bb"
#     u2.last_name = "bb"
#     context = {'contacts': [u1, u2]}
#     return render(request, 'chat_channel/popup_chat_page.html', context=context)

@login_required
def chat_page_with_contact(request, to_user_id):
    """View function for home page of site."""
    # TODO adding auth and getting prev messages after adding user table

    to_user = get_object_or_404(User, pk=to_user_id)
    """ creating contact if does not exist """
    to_user_contact_list = ChatContact.objects.filter(owner=request.user, contact_user=to_user)
    if to_user_contact_list.count() == 0:
        user_contact = ChatContact()
        user_contact.owner = request.user
        user_contact.contact_user = to_user
        user_contact.save()
    else:
        user_contact = to_user_contact_list[0]

    to_user_contact_list = ChatContact.objects.filter(contact_user=request.user, owner=to_user)
    if to_user_contact_list.count() == 0:
        to_user_contact = ChatContact()
        to_user_contact.contact_user = request.user
        to_user_contact.owner = to_user
        to_user_contact.save()

    """ retrieving contacts """

    contacts = ChatContact.objects.filter(owner=request.user)

    context = {'contacts': contacts, 'to_contact_id': user_contact.pk, 'to_user_id': user_contact.contact_user.pk}
    return render(request, 'chat_channel/chat_page_with_contact.html', context=context)
