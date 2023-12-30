from django.contrib.auth import get_user_model
from rest_framework import serializers

from userapp.models import FriendRequests, FriendshipModel

User = get_user_model()


class UsersAllSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )


class GetFriendSerializer(serializers.ModelSerializer):
    friends = FriendsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id",
                  "username",
                  "friends",)


class FromUserFriendRequestSerializer(serializers.ModelSerializer):
    from_user = FriendsSerializer()

    # to_user = FriendsSerializer()

    class Meta:
        model = FriendRequests
        fields = ("id",
                  # "to_user",
                  "from_user",
                  "datetime",
                  # "accepted",
                  )


class ToUserFriendRequestSerializer(serializers.ModelSerializer):
    # from_user = FriendsSerializer()
    to_user = FriendsSerializer()

    class Meta:
        model = FriendRequests
        fields = ("id",
                  "to_user",
                  # "from_user",
                  "datetime",
                  # "accepted",
                  )


class GetFriendRequestsSerializer(serializers.ModelSerializer):
    # friends = FriendsSerializer(many=True, read_only=True)
    friend_requests = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id",
                  "username",
                  "friend_requests",
                  )

    def get_friend_requests(self, obj):
        friend_requests = obj.friend_requests.only("id", "from_user")
        return FromUserFriendRequestSerializer(friend_requests, many=True).data


class FrienndsOfUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
        ]


class FriendshipSerializer(serializers.ModelSerializer):
    friend_data = serializers.SerializerMethodField()

    class Meta:
        model = FriendshipModel
        fields = [
            "datetime",
            "friend_data",
        ]

    def get_friend_data(self, obj):
        user = obj.id_other_user
        return FrienndsOfUserSerializers(user).data
