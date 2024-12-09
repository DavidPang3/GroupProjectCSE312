from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
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
stats_collection = db["stats"]


#html
def home(request): #if token exists, match it to user_collection in db and retrieve username
    #chat_collection.delete_many({})  
    #user_collection.delete_many({})
    #stats_collection.delete_many({})
    token = request.COOKIES.get('token')
    username = "Guest"
    if token:
        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        stored_user = user_collection.find_one({"token": hashed_token})
        if stored_user:
            username = stored_user.get('username') + " / Logout"
            username2 = stored_user.get('username')

            initialfind = stats_collection.find_one({"username": username2}) #stats_collection.insert_one({"username": username, "requestsmade": "0", "statsrequestmade": "0", "messages_sent": "0", "images_sent": "0", "loggedin": "0"})
            homespage = int(initialfind.get("requestsmade"))
            homespage += 1
            stats_collection.update_one({"username": username2}, {"$set": {"requestsmade": str(homespage)}})
        else:
            username = "Guest"
    else:
        username = "Guest"

    return render(request, 'index.html', {'username': username})


def loginregister(request):
    token = request.COOKIES.get('token')
    print(f"UR TOKEN IS {token}")
    username = "Guest / Logout"
    if token:
        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        stored_user = user_collection.find_one({"token": hashed_token})
        if stored_user:
            username = stored_user.get('username') + " / Logout"
            username2 = stored_user.get('username')
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

    stats_collection.insert_one({"username": username, "requestsmade": "0", "statsrequestmade": "0", "messages_sent": "0", "images_sent": "0", "loggedin": "0"})
    if(auth.validate_password(password) == True):
        salt = bcrypt.gensalt()
        hashedpassword = bcrypt.hashpw(password.encode(), salt)
        user_collection.insert_one({"username": username, "password": hashedpassword})
        return(redirect("/loginregister/"))
    else:
        return (HttpResponse("Unacceptable Password! Requirements: minimum length: 8, one capital, one letter, one number, one special character", status=401))

        

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
                response.set_cookie('token', token, max_age=datetime.timedelta(hours=1), httponly=True, path='/')
                initialfind = stats_collection.find_one({"username": username})
                loggedin = int(initialfind.get("loggedin"))
                loggedin += 1
                stats_collection.update_one({"username": username}, {"$set": {"loggedin": str(loggedin)}})

                return (response)
            else:
                return (HttpResponse("Wrong password", status=401))
        else:
            return (HttpResponse("Incorrect Password or Username", status=401))


def logoutacc(request):
        currenttoken = request.COOKIES.get("token")
        if(currenttoken):
            hashedcurrent = hashlib.sha256(currenttoken.encode()).hexdigest() 
            user_collection.update_one({"token": hashedcurrent}, {"$set": {"token": ""}}) #invalidate token by setting to blank
        
            response = HttpResponseRedirect("/")
            response.set_cookie('token','',max_age=0,httponly=True,path='/')
            return response
        else:
            return (HttpResponse("Guests cannot logout", status=401))

def stats(request):
    token = request.COOKIES.get('token')
    print(f"UR TOKEN IS {token}")
    username = "Guest"
    if token:
            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            stored_user = user_collection.find_one({"token": hashed_token})
            if stored_user:
                username = stored_user.get('username') + " / Logout"
                username2 = stored_user.get('username')
                initialfind = stats_collection.find_one({"username": username2})
                statspage = int(initialfind.get("statsrequestmade"))
                statspage += 1
                stats_collection.update_one({"username": username2}, {"$set": {"statsrequestmade": str(statspage)}})

                homerequestsmade = initialfind.get("requestsmade")
                statsrequestmade = initialfind.get("statsrequestmade")
                messages_sent = initialfind.get("messages_sent")
                images_sent = initialfind.get("images_sent")
                loggedin = initialfind.get("loggedin")

                return render(request, 'stats.html', {'username': username, 'username2': username2, 'homerequestsmade': homerequestsmade, 'statsrequestmade': statsrequestmade, 'messages_sent': messages_sent, 'images_sent': images_sent, 'loggedin': loggedin})

            else:
                return HttpResponseNotFound("User must be logged in to access the stats page")
    else:
            return HttpResponseNotFound("User must be logged in to access the stats page")
    
  

    
        
    


        #form = UploadFileForm()
    #return render(request, "room.html", {"form": form})