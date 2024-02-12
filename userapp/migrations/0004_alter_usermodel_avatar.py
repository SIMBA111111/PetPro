# Generated by Django 5.0 on 2024-02-11 14:36

import userapp.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_alter_usermodel_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/avatars/%y/%m/%d', validators=[userapp.validators.AvatarSizeValidator]),
        ),
    ]