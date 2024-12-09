import json
import hashlib
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from pymongo import MongoClient
from pytz import timezone
from datetime import datetime
import time
import threading
from app.views import stats_collection

# MongoDB setup
easterntime = timezone('US/Eastern')

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

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        async_to_sync(self.channel_layer.group_add)(self.global_group_name, self.channel_name)

        for msg in chat_collection.find():
            if "text" in msg:
                async_to_sync(self.channel_layer.group_send)( 
                    self.room_group_name, {"type": "chat.message", "message": f"{msg['text']}"}
                )

        self.accept()

        self.start_time_updates()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.global_group_name, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if "<img" in message:
            chat_collection.insert_one({'text': message})
            async_to_sync(self.channel_layer.group_send)( 
                self.global_group_name, {"type": "chat.message", "message": message}
            )
        else:
            initialfind = stats_collection.find_one({"username": self.username})
            messages_sent = int(initialfind.get("messages_sent"))
            messages_sent += 1
            stats_collection.update_one({"username": self.username}, {"$set": {"messages_sent": str(messages_sent)}}) 

            current_time = self.get_current_time()
            chat_collection.insert_one({'text': f'({current_time}) {self.username}: {message}'})
            async_to_sync(self.channel_layer.group_send)( 
                self.global_group_name, {"type": "chat.message", "message": f"({current_time}) {self.username}: {message}"}
            )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))


    #TIME UPDATE AND RETREIVALS
    def get_current_time(self):
        current_time = datetime.now(easterntime)
        return current_time.strftime('%I:%M:%S %p') #hours, minutes, seconds, meridian

    def send_time(self):
        current_time = self.get_current_time()
        async_to_sync(self.channel_layer.group_send)(
            self.global_group_name,
            {"type": "chat.message", "message": f"Current time: {current_time}"}
        )

    def start_time_updates(self):
        def time_update_loop():
            while True:
                self.send_time()
                time.sleep(1)

        thread = threading.Thread(target=time_update_loop, daemon=True) #use threading to stop hang!!
        thread.start()
