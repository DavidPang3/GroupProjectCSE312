import hashlib
from app.views import user_collection
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from pymongo import MongoClient #pip install pymongo
from django import forms
from .forms import UploadFileForm, handle_uploaded_file
import time
from app.views import mongo_client, user_collection, db, chat_collection, stats_collection
import threading
from pytz import timezone
from datetime import datetime, timedelta




# Create your views here.
def room(request):
    token = request.COOKIES.get('token')
    print(f"UR TOKEN IS {token}")
    username = "Guest"
    if token:
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            stored_user = user_collection.find_one({"token": hashed_token})
            if stored_user:
                username = stored_user.get('username') + " / Logout"
            else:
                return HttpResponseNotFound("User must be logged in to access the community page")
    else:
            return HttpResponseNotFound("User must be logged in to access the community page")

    return render(request, 'chat/room.html', {'username': username, 'current_time': current_time})

def uploads(request): #this is indeed called on /uploads/ path
    token = request.COOKIES.get('token')
    print(f"UR TOKEN IS {token}")
    username = "Guest"
    if token:
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            stored_user = user_collection.find_one({"token": hashed_token})
            if stored_user:
                username = stored_user.get('username')

                initialfind = stats_collection.find_one({"username": username})
                images_sent = int(initialfind.get("images_sent"))
                images_sent += 1
                stats_collection.update_one({"username": username}, {"$set": {"images_sent": str(images_sent)}})
            
    print("uploads was called")
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"], request, username, current_time)
            time.sleep(1)
            return HttpResponseRedirect("/chat/") #doesn't redirect because we using websockets stream 
    else:
        return HttpResponseNotFound("Page not found")
    

current_time = 0

def schedule(request):
    statictime = current_time
    token = request.COOKIES.get('token')
    print(f"UR TOKEN IS {token}")
    username = "Guest"
    if token:
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            stored_user = user_collection.find_one({"token": hashed_token})
            if stored_user:
                username = stored_user.get('username')

    delay = request.POST.get("timestamp")
    delay = int(delay)
    message = request.POST.get("delayedmessage")
    time.sleep(delay)
    chat_collection.insert_one({"text": f'({current_time}) {username}: {message}'})
    return render(request, 'chat/room.html', {'current_time': statictime})

