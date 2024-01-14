from django.urls import path

from userapp import views

urlpatterns = [
    path('all-my-fr', views.GetAllFriendsAllUsersAPIVIEW.as_view(), name="all-my-fr"),  # выводит всех моих друзей
    path('login', views.Login.as_view(), name='login'),  # аутентификация
    path('register', views.Register.as_view(), name='register'),  # аутентификация
    path('', views.UsersAllAPIVIEW.as_view(), name="users-list"),  # выводит всех юзеров приложения
    path('my-chats', views.AllMyChats.as_view(), name="my-chats"),  # выводит всех юзеров приложения
    path('my-group-chats', views.AllMyGroupChats.as_view(), name="my-group-chats"),  # выводит всех юзеров приложения
    path('qw/<int:id>', views.GetFriendRequestsAPIVIEW.as_view(), name="requests-fr---"),
    # выводит запросы на дружбу определённого юзера
    path('profile/<str:username>', views.SendFriendRequestAPIVIEW.as_view(), name="profile"),
    # отправляет запрос на дружбу от авторизированного юзера выбранному
    path('accept/', views.AcceptFriendRequest.as_view(), name="requests-fr"),
    # принимает запрос на дружбу и добавляет в друзья
    path('request-to-group-room/', views.RequestToGroupRoom.as_view(), name="requests-to-group-room"),  #
    path('create-group-room/', views.CreateGroupRoom.as_view(), name="create-group-room"),  #
]
