from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.db import models

User = get_user_model()


class EmailCodeModel(models.Model):
    user = models.ForeignKey(User, models.CASCADE, "email_code", verbose_name="Юзер")
    code = models.SmallIntegerField(verbose_name="Код привязки почты", unique=True,
                                    validators=[MinLengthValidator(10), MaxLengthValidator(10)])
