from django.contrib import admin

from chat.models import ChatModel, MessageModel


@admin.register(ChatModel)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(MessageModel)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "chat_name", "author"]
