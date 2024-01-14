from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, TemplateView, ListView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from userapp import forms
from userapp import serializers
from userapp import models
from chat.models import ChatModel, GroupChatModel, RequestToAddGroupChatModel

# from userapp.views import RequestToGroupRoom

User = get_user_model()


class AllMyGroupChats(ListView):
    queryset = None

    def get(self, request, *args, **kwargs):
        group_chats = GroupChatModel.objects.filter(users=request.user)
        print(group_chats)
        return render(request, "userapp/my-groups-chats.html", context={"group_chats": group_chats})


class AllMyChats(ListView):
    queryset = None

    def get(self, request, *args, **kwargs):
        chats = ChatModel.objects.select_related("username_two", "username_one").filter(
            Q(username_one__username=request.user) | Q(username_two__username=request.user))
        return render(request, "userapp/my-chats.html", context={"chats": chats})


class UsersAllAPIVIEW(APIView):
    queryset = User.objects.all()
    serializer_class = serializers.UsersAllSerializers

    def get(self, request, *args, **kwargs):
        users = User.objects.exclude(username=request.user)
        return render(request, "userapp/users_all.html", context={"users": users})


# Посмотреть всех друзей аутентифицированного юзера
class GetAllFriendsAllUsersAPIVIEW(generics.ListAPIView):
    queryset = None
    serializer_class = serializers.GetFriendSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        friends = models.FriendshipModel.objects.select_related("id_other_user").filter(id_user=request.user.id)
        # friends_serialized = serializers.FriendshipSerializer(friends, many=True)
        return render(request, "userapp/my_friends.html", context={"friends": friends})
        # return Response(data={"friends": friends_serialized.data})


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
        username_other = kwargs["username"]

        if request.user == username_other:
            return HttpResponseNotFound()

        chat = ChatModel.objects.filter(
            Q(username_one__username=username_other) | Q(username_one__username=request.user),
            Q(username_two__username=username_other) | Q(username_two__username=request.user),
        )
        if not chat.exists():
            user_other = User.objects.get(username=username_other)
            user_from = User.objects.get(username=request.user)
            ChatModel.objects.create(username_one=user_other, username_two=user_from)

        return render(request, "userapp/any_profile.html",
                      context={"username_other": username_other, "chat_number": chat[0].id})

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


class Register(CreateView):
    template_name = "userapp/register.html"
    form_class = forms.RegisterForm
    success_url = reverse_lazy("login")


class RequestToGroupRoom(ListView):
    queryset = None

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        data = user.to_user_request_add_to_group_chat.filter(accepted=False)

        return render(request, template_name="userapp/requests_to_group_chat.html", context={"data": data})

    def post(self, request, *args, **kwargs):
        obj = RequestToAddGroupChatModel.objects.get(id=request.POST.get("id_request"))
        obj.accepted = True
        obj.save()

        user_id = request.user.id
        to_user = User.objects.get(id=user_id)
        group_chat_name = request.POST.get("group_chat_name")

        group_chat = GroupChatModel.objects.get(id=group_chat_name)
        group_chat.users.add(to_user)

        return render(request, "userapp/requests_to_group_chat.html")


class CreateGroupRoom(View):
    def get(self, request, *args, **kwargs):
        return render(request, "userapp/create_new_group_room.html")

    def post(self, request, *args, **kwargs):
        group_chat_name = request.POST.get('group_name')

        new_group_chat = GroupChatModel.objects.create(name=group_chat_name)
        new_group_chat.users.add(request.user)

        return redirect("my-group-chats")
