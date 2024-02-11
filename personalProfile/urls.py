from django.urls import path

from personalProfile import views

urlpatterns = [
    path("avatar", views.Avavtar.as_view(), name="avatar"),
]
