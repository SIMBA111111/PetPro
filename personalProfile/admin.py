from django.contrib import admin

from personalProfile.models import EmailCodeModel


@admin.register(EmailCodeModel)
class EmailCodeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "code", ]
