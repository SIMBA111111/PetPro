# consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

from chat.models import ChatModel, MessageModel

User = get_user_model()


### НАДО ЗДЕСЬ ДОБАВИТЬ СОХРАНЕНИЕ СООБЩЕНИЙ И КАК-ТО ВЫЯВЛЯТЬ ЧАТ НУЖНЫЙ
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        print(self.room_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Принимает сообщения с фронта и отправляет их конкретному обработчику
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        author = text_data_json["author"]
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat.message", "author": author, "message": message},
        )

    # Отправляет сообщения
    def chat_message(self, event):
        author = event["author"]
        message = event["message"]

        current_user = User.objects.get(username=author)
        current_chat = ChatModel.objects.get(id=self.scope["url_route"]["kwargs"]["room_name"])
        # print(current_chat)
        # print(current_user)
        MessageModel.objects.create(text=message, author=current_user, chat_name=current_chat)

        # отправляет через веб сокет обратно на клиент. НО КАКОЙ МЕТОД НА КЛИЕНТЕ ИХ ПРИНИМАЕТ?
        self.send(
            text_data=json.dumps({"author": author, "message": message}),
        )
