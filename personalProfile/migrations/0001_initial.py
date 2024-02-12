# Generated by Django 5.0 on 2024-02-12 17:43

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.SmallIntegerField(unique=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(10)], verbose_name='Код привязки почты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_code', to=settings.AUTH_USER_MODEL, verbose_name='Юзер')),
            ],
        ),
    ]