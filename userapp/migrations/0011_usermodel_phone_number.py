# Generated by Django 5.0 on 2024-02-11 15:36

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0010_usermodel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=12, null=True, region=None, verbose_name='Номер телефона'),
        ),
    ]