from django.contrib import admin

from chat.models import ChatModel, MessageModel, GroupChatModel, RequestToAddGroupChatModel


@admin.register(ChatModel)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(MessageModel)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "chat_name", "group_chat_name", "author"]


@admin.register(GroupChatModel)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ["id", ]


@admin.register(RequestToAddGroupChatModel)
class RequestToAddGroupChatAdmin(admin.ModelAdmin):
    list_display = ["id", ]
