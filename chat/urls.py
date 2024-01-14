from django.urls import path

from chat import views

urlpatterns = [
    # path("", views.index, name="index"),
    path("add/", views.RequestToAddGroupChat.as_view(), name="add"),
    path("<str:room_name>/", views.room, name="room"),
    path("group/<str:group_room_name>/", views.group_room, name="group-room"),
]
