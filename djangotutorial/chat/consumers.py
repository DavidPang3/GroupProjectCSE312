import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import hashlib
from pymongo import MongoClient
from django.shortcuts import redirect

# MongoDB setup
mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
chat_collection = db["chat"]
user_collection = db["user"]

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        token = self.scope.get('cookies', {}).get('token')
        username = "Guest"
        if token:
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            stored_user = user_collection.find_one({"token": hashed_token})
            if stored_user:
                username = stored_user.get('username')


        self.username = username
        self.room_name = 'chat'
        self.room_group_name = f"chat_{self.username}"  
        self.global_group_name = "chat_global"  



        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        async_to_sync(self.channel_layer.group_add)(
            self.global_group_name, self.channel_name
        )

        for msg in chat_collection.find():
            if "text" in msg:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "chat.message", "message": f"{msg['text']}"}
                )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.global_group_name, self.channel_name
        )


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if "<img" in message:  
            chat_collection.insert_one({'text': message})
            async_to_sync(self.channel_layer.group_send)(
                self.global_group_name, {"type": "chat.message", "message": message}
                
            )
            return redirect('/chat/')
        else:
        
            chat_collection.insert_one({'text': f'{self.username}: {message}'})
            async_to_sync(self.channel_layer.group_send)(
                self.global_group_name, {"type": "chat.message", "message": f"{self.username}: {message}"}
            )
            
     

    def chat_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({"message": message}))