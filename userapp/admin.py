from django.contrib import admin

from userapp import models


class UserInline(admin.StackedInline):
    model = models.FriendshipModel
    extra = 5
    fk_name = "id_user"


class FriendsInline(admin.StackedInline):
    model = models.FriendshipModel
    extra = 5
    fk_name = "id_other_user"


@admin.register(models.UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id",)
    inlines = (UserInline,)


@admin.register(models.FriendshipModel)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(models.FriendRequests)
class FriendRequestsAdmin(admin.ModelAdmin):
    list_display = ("id",)
