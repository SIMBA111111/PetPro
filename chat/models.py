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
    author = models.ForeignKey(User, models.DO_NOTHING, "author_messages")
    datetime = models.DateTimeField(auto_now_add=True)
    chat_name = models.ForeignKey(ChatModel, models.CASCADE, "chat_name_messages")
