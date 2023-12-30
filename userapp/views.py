from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import FormView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from userapp import forms
from userapp import serializers
from userapp import models

User = get_user_model()


class UsersAllAPIVIEW(APIView):
    queryset = User.objects.all()
    serializer_class = serializers.UsersAllSerializers

    def get(self, request, *args, **kwargs):
        users = User.objects.exclude(username=request.user)
        auth_user = request.user
        return render(request, "userapp/users_all.html", context={"users": users, "auth_user": auth_user})


# Посмотреть всех друзей аутентифицированного юзера
class GetAllFriendsAllUsersAPIVIEW(generics.ListAPIView):
    queryset = None
    serializer_class = serializers.GetFriendSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        friends = models.FriendshipModel.objects.filter(id_user=request.user.id).only("datetime")
        friends_serialized = serializers.FriendshipSerializer(friends, many=True)
        return Response(data={"friends": friends_serialized.data})


# Посмотреть запросы на дружбу опредлённого юзера
class GetFriendRequestsAPIVIEW(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.GetFriendRequestsSerializer
    lookup_field = "id"


# Отправить заявку в друзья
class SendFriendRequestAPIVIEW(generics.ListCreateAPIView):
    queryset = None
    serializer_class = serializers.ToUserFriendRequestSerializer
    lookup_field = "username"

    def get(self, request, *args, **kwargs):
        return render(request, "userapp/any_profile.html")

    def post(self, request, *args, **kwargs):
        to_user_username = kwargs["username"]
        to_user = User.objects.get(username=to_user_username)
        from_user = request.user
        obj = models.FriendRequests.objects.create(to_user=to_user,
                                                   from_user=from_user,
                                                   )
        return redirect("users-list")


# Подтвердить/показать заявку в друзья
class AcceptFriendRequest(generics.GenericAPIView):
    queryset = None
    serializer_class = serializers.FromUserFriendRequestSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    # вывести все заявки
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        data = user.friend_requests.filter(accepted=False)
        return render(request, template_name="userapp/friend_requests.html", context={"data": data})

    # принять заявку в друзья
    def post(self, request, *args, **kwargs):
        obj = models.FriendRequests.objects.get(id=request.data["id_request"])
        obj.accepted = True
        obj.save()

        user_id = request.user.id
        to_user = User.objects.get(id=user_id)
        from_user_username = request.data["from_user"]
        from_user = User.objects.get(username=from_user_username)
        to_user.friends.add(from_user)

        return Response(template_name="userapp/friend_requests.html")


# аутентификация
class Login(FormView):
    form_class = forms.LoginForm
    template_name = "userapp/login.html"

    # аутентифицироваться
    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("users-list")
        else:
            return Response()
