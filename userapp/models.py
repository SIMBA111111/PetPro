from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class UserModel(AbstractUser):
    friends = models.ManyToManyField("self", blank=True, through="FriendshipModel", )
    # avatar = models.FileField

class FriendshipModel(models.Model):
    id_user = models.ForeignKey(UserModel, models.SET_NULL, "user", null=True)
    id_other_user = models.ForeignKey(UserModel, models.SET_NULL, "other_user", null=True)
    datetime = models.DateTimeField(auto_now_add=True)


class FriendRequests(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    to_user = models.ForeignKey(UserModel, models.CASCADE, "friend_requests", )
    from_user = models.ForeignKey(UserModel, models.CASCADE, )
    accepted = models.BooleanField(default=False, )

    class Meta:
        unique_together = [["to_user", "from_user"], ]
