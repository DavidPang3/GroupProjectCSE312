from django import forms
import os
from django.conf import settings
from pymongo import MongoClient
from app.views import mongo_client, user_collection, db, chat_collection
import time

image_collection = db["images"]

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

def handle_uploaded_file(f, request, username, current_time):
    title = request.POST.get('title')
    title = title.replace(" ", "_").replace("/", "_")  #parse all filenames security
    newname = f.name.replace(" ", "_").replace("/", "_")  
    file_name = f'{title}_{newname}'  
    file_path = os.path.join('/root/djangotutorial/chat/images', file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as destination:
        for chunk in f.chunks():  
            destination.write(chunk) 

    realfilepath = f'/chat/images/{file_name}'
    imgtag = f'<img src="{realfilepath}" alt="Image" />'
    chat_collection.insert_one({"text": f'({current_time}) {username}: {imgtag}'})

