import hashlib
from app.views import user_collection
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from pymongo import MongoClient #pip install pymongo
from django import forms
from .forms import UploadFileForm, handle_uploaded_file


# Create your views here. hhhhh
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

    return render(request, 'chat/room.html', {'username': username})

def uploads(request): #this is indeed called on /uploads/ path

    token = request.COOKIES.get('token')
    username = "Guest"
    if token:
        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        stored_user = user_collection.find_one({"token": hashed_token})
        if stored_user:
            username = stored_user.get('username') + " / Logout"
        else:
            username = "Guest"
    else:
        username = "Guest"

    print("uploads was called")
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"], request, username)
            return HttpResponseRedirect("/chat/")
    else:
        return HttpResponseNotFound("Page not found")