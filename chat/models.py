from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ChatModel(models.Model):
    username_one = models.ForeignKey(User, models.DO_NOTHING, "chat_username_one")
    username_two = models.ForeignKey(User, models.DO_NOTHING, "chat_username_two")
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('username_two', 'username_one',)

    def __str__(self):
        return f"{self.pk}"


class MessageModel(models.Model):
    text = models.CharField(max_length=255, )
    image = models.ImageField(upload_to="chat/static/images/%Y/%M/%D", blank=True, null=True)
    author = models.ForeignKey(User, models.DO_NOTHING, "author_messages")
    datetime = models.DateTimeField(auto_now_add=True)
    chat_name = models.ForeignKey(ChatModel, models.CASCADE, "chat_name_messages", null=True, blank=True)
    group_chat_name = models.ForeignKey("GroupChatModel", models.CASCADE, "group_chat_name_messages", null=True,
                                        blank=True)


class GroupChatModel(models.Model):
    name = models.CharField(max_length=33, )
    users = models.ManyToManyField(User, "group_chats", )
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}'


class RequestToAddGroupChatModel(models.Model):
    group_chat_name = models.ForeignKey(GroupChatModel, models.CASCADE, "group_chats_name", )
    from_user = models.ForeignKey(User, models.CASCADE, "from_user_request_add_to_group_chat", )
    to_user = models.ForeignKey(User, models.CASCADE, "to_user_request_add_to_group_chat", )
    accepted = models.BooleanField(default=False, )

    # datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["group_chat_name", "to_user"], ]
