from django.shortcuts import render

from chat.models import ChatModel


def index(request):
    return render(request, "chat/chat-name.html")


### МОЖНО ЗДЕСЬ ПОЛУЧАТЬ НОМЕР ЧАТА, ОТРПАВЛЯТЬ ЕГО НА JS, ТАМ ВМЕСТЕ СО ВСЕМИ ДАННЫМИ ВЫВОДИТЬ В БЭК.
### НО ЛУЧШЕ СРАЗУ В КОНСЮМЕРЕ ПОЛУЧАТЬ ЧЕРЕЗ SCOPE
def room(request, room_name):
    print("room")
    current_chat = ChatModel.objects.get(id=room_name)
    messages = current_chat.chat_name_messages.select_related("author").all()
    return render(request, "chat/room.html", {"room_name": room_name, "messages": messages})
