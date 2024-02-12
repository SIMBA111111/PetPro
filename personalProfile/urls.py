from django.urls import path

from personalProfile import views

urlpatterns = [
    path("avatar", views.Avavtar.as_view(), name="avatar"),
    path("email-code", views.EmailCode.as_view(), name="email-code"),
    path("set-email", views.set_email, name="set-email"),
]
