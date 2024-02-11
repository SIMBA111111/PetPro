from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from phonenumber_field.modelfields import PhoneNumberField

from userapp.validators import AvatarSizeValidator


class UserModel(AbstractUser):
    friends = models.ManyToManyField("self", blank=True, through="FriendshipModel", )
    avatar = models.ImageField(upload_to="avatars/%y/%m/%d", blank=True, null=True, validators=[AvatarSizeValidator, ])
    middle_name = models.CharField(max_length=55, blank=True, null=True, verbose_name="Фамилия")
    description = models.TextField(max_length=255, verbose_name="Описание профиля", null=True, blank=True)
    phone_number = PhoneNumberField(max_length=12, verbose_name="Номер телефона", null=True, blank=True, )


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
