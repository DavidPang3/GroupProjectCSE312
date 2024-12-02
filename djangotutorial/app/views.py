from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import os
import uuid
from pymongo import MongoClient #pip install pymongo
import bcrypt
import hashlib
import json
import datetime
from mysite import auth



mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
chat_collection = db["chat"]
user_collection = db["user"]


#html
def home(request): #if token exists, match it to user_collection in db and retrieve username
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

    return render(request, 'index.html', {'username': username})


def loginregister(request):
    token = request.COOKIES.get('token')
    print(f"UR TOKEN IS {token}")
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

    return render(request, 'loginregister.html', {'username': username})

#css
def homecss(request):
    file_path = os.path.join('mysite', 'static', 'css', 'index.css')
    with open(file_path, 'r') as file:  
        css_content = file.read() 
    return HttpResponse(css_content, content_type='text/css')  

def loginregistercss(request):
    file_path = os.path.join('mysite', 'static', 'css', 'loginregister.css')
    with open(file_path, 'r') as file:  
        css_content = file.read() 
    return HttpResponse(css_content, content_type='text/css')  

def navbarcss(request):
    file_path = os.path.join('mysite', 'static', 'css', 'navbar.css')
    with open(file_path, 'r') as file: 
        css_content = file.read()  
    return HttpResponse(css_content, content_type='text/css')  


#javascript
def javascript(request):
    pass 


#images
def homebackgroundimage(request):
    file_path = os.path.join('mysite', 'static', 'images', 'backgroundhome.jpg')
    with open(file_path, 'rb') as file:
        image_content = file.read()
    return HttpResponse(image_content, content_type='image/jpeg')



#loginregister

def registeracc(request):
   # if request.method == "POST":
    username = request.POST.get("username")  
    password = request.POST.get("password")  
    print(f"your username is {username} and your pass is {password}")

    if(auth.validate_password(password) == True):
        salt = bcrypt.gensalt()
        hashedpassword = bcrypt.hashpw(password.encode(), salt)
        user_collection.insert_one({"username": username, "password": hashedpassword})

    
        return(redirect("/loginregister/"))


def loginacc(request):
        username = request.POST.get("username")  
        password = request.POST.get("password")  
        print(f"your ATTEMPTED username is {username} and your pass is {password}")
        storeduser = user_collection.find_one({"username": username})
        token = ""
        
        if(storeduser):
            storedpass = storeduser["password"]
            check = bcrypt.checkpw(password.encode(), storedpass)
            print(f"check is {check}")

            if(check == True):
                token = str(uuid.uuid4())
                hashedtoken = hashlib.sha256(token.encode()).hexdigest() 
                user_collection.update_one({"username":username}, {"$set": {"token":hashedtoken}})
                response = HttpResponseRedirect("/loginregister/")
                response.set_cookie(
                            'token', 
                            token, 
                            max_age=datetime.timedelta(hours=1),
                            httponly=True,
                            #secure=True,
                            path='/'
                        )
                        
                return (response)
            else:
                return (HttpResponse("Wrong password", status=401))
        else:
            return (HttpResponse(storeduser))


def logoutacc(request):
        currenttoken = request.COOKIES.get("token")
        hashedcurrent = hashlib.sha256(currenttoken.encode()).hexdigest() 
        user_collection.update_one({"token": hashedcurrent}, {"$set": {"token": ""}}) #invalidate token by setting to blank
      
        response = HttpResponseRedirect("/")
        response.set_cookie(
            'token',
            '',
            max_age=0,
            httponly=True,
            path='/'
        )
        return response

    
    


        #form = UploadFileForm()
    #return render(request, "room.html", {"form": form})