from django.urls import path

from userapp import views

urlpatterns = [
    path('all-my-fr', views.GetAllFriendsAllUsersAPIVIEW.as_view()), # выводит всех моих друзей
    path('login', views.Login.as_view(), name='login'), # аутентификация
    path('users-list', views.UsersAllAPIVIEW.as_view(), name="users-list"), # выводит всех юзеров приложения
    path('qw/<int:id>', views.GetFriendRequestsAPIVIEW.as_view()), # выводит запросы на дружбу определённого юзера
    path('profile/<str:username>', views.SendFriendRequestAPIVIEW.as_view(), name="profile"), # отправляет запрос на дружбу от авторизированного юзера выбранному
    path('accept/', views.AcceptFriendRequest.as_view()), # принимает запрос на дружбу и добавляет в друзья
]
