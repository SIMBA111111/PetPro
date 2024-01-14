from urllib.parse import parse_qs

from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import generic
from rest_framework.response import Response

from chat.models import ChatModel, GroupChatModel, RequestToAddGroupChatModel

User = get_user_model()


def index(request):
    return render(request, "chat/chat-name.html")


def room(request, room_name):
    print("личный чат")
    print(request.user)
    current_chat = ChatModel.objects.get(id=room_name)
    messages = current_chat.chat_name_messages.select_related("author").all()
    return render(request, "chat/room.html", {"room_name": room_name, "messages": messages})


def group_room(request, group_room_name):
    print("груп рума")

    current_group_chat = GroupChatModel.objects.get(id=group_room_name)
    users_this_group_chat = current_group_chat.users.all()

    if request.user in users_this_group_chat:
        messages = current_group_chat.group_chat_name_messages.select_related("author").all()
        return render(request, "chat/group-room.html",
                      {"group_room_name": group_room_name, "messages": messages,
                       "current_group_chat": users_this_group_chat})
    else:
        return HttpResponseNotFound()


class RequestToAddGroupChat(generic.View):

    def post(self, request, *args, **kwargs):
        request_body = request.body.decode('utf-8')

        parsed_body = parse_qs(request_body)

        message_value_username = parsed_body.get('message', [''])[0]

        ToUser = User.objects.get(username=message_value_username)

        last_digit = None
        for char in reversed(request.headers["Referer"]):
            if char.isdigit():
                last_digit = char
                break

        currently_group_room = GroupChatModel.objects.get(id=last_digit)

        RequestToAddGroupChatModel.objects.create(group_chat_name=currently_group_room,
                                                  from_user=request.user,
                                                  to_user=ToUser,
                                                  )

        return redirect(request.headers["Referer"])
