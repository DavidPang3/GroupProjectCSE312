#from .request import Request
#from request import Request
#review query strings lecture slide 
#unfinished 
#https://duckduckgo.com/?q=web+development&ia=web example query
#from request import Request
#ready to submit

'''
    if(string == "%20" or string == "+"):
        newstring = " "
        return newstring
    '''

def convert(string):
    newstring = ""
    if(string == "%20" or string == "+"):
        newstring = " "
        return newstring
    elif(string == "%21"): 
        newstring = "!"
        return newstring
    elif(string == "%40"):
        newstring = "@"
        return newstring
    elif(string == "%23"):
        newstring = "#"
        return newstring
    elif(string == "%24"):
        newstring = "$"
        return newstring
    elif(string == "%25"):
        newstring = "%"
        return newstring
    elif(string == "%5E"):
        newstring = "^"
        return newstring
    elif(string == "%26"):
        newstring = "&"
        return newstring
    # WTF IS '(', ')' I GUESS ITS COMMA?
    elif(string == "%28"):
        newstring = "("
        return newstring
    elif(string == "%29"):
        newstring = ")"
        return newstring
    elif(string == "%2D"):
        newstring = "-"
        return newstring
    elif (string == "%5F"):
        newstring = "_"
        return newstring
    elif(string == "%3D"):
        newstring = "="
        return newstring
    else:
        return string


def extract_credentials(request):
    list1 = []
    path = request.body.decode('utf-8')
    #path = request.path
    string = path #.decode('utf-8') %20 or + is a space
    #write code that parses by finding username and password in string
   
    #query = string.split('?')[1] #this causes list index out of range
    
    keyvalue = string.split('&')
    
    #username=david&password=somethingwong&testing=bruh
   
    structure = {}
    for x in keyvalue:
        x = x.strip()
        store = x.split('=')
        structure[store[0].strip()] = store[1].strip()


    username = structure["username"]
    password = structure["password"]

    newusername = username
    newpassword = ""

    
    index = 0
    while index < (len(password)):
        if(password[index] == "%"): # %25 stores temp as %2 and converts it
            temp = ""
            temp += password[index]
            index +=1
            temp += password[index]
            index +=1
            temp += password[index]
            newpassword += convert(temp) 
        else:
            newpassword += password[index]
        index+=1
    

    
            
    list1.append(newusername)
    list1.append(newpassword)

    return list1


def validate_password(string):
    check = True

    #length at least 8
    if(len(string) >= 8):
        pass 
    else:
        print("Failed length requirement")
        return False

    #contains one lower char
    for x in string:
        if x.islower():
            check = True
            break
        else:
            check = False
    
    if(check == False): 
        print("Failed lower case")
        return False

    #contains one upper char
    for x in string:
        if x.isupper():
            check = True
            break
        else:
            check = False
    
    if(check == False): 
        print("Failed upper case")
        return False

    #contains one number 
    for x in string:
        if x.isdigit():
            check = True
            break
        else:
            check = False

    if(check == False): 
        print("Failed number requirement")
        return False

    #contains one special character
    special = ['!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '=']
    for x in string:
        for y in special:
            if(x==y):
                print(f"A MATCH IS FOUND! {x} == {y}, breaking loop now")
                check = True
                break
            else:
                print(f"false, {x} does not equal {y}")
                check = False
        if(check==True):
            break
    
    if(check == False): 
        print("failed special char requirement")
        return False

    #contains invalid character 
    for x in string:
        if(x.islower() or x.isupper() or x.isdigit()):
            check = True
        else:
            for y in special:
                if(x == y):
                    print(f"check = true, {x} == {y}")
                    check = True
                    break
                else:
                    print(f"false, {x} does not equal {y}")
                    check = False
            if(check == False):
                print(f"failed invalid character = {x}")
                return False
    return True


def test2():
    print("running test2")
    request = Request(b'POST /path1231 HTTP/1.1\r\n Host:       localhost:8080   \r\n   Connection:  keep-alive \r\n  headerasdiunasoudn:    asdasd \r\n   asodunasdheader2:asdoaisnd \r\n  header3forbettertesting:VALUE!!!\r\n   Cookie: id1    = thisdobeacookie; id2=   thisanothercookie; id3   =   thisathirdcookie\r\n\r\nusername=daveedas& password = Wasd!1231%25123%21%40haha!')
    extract_credentials(request)
    list1 = extract_credentials(request)
    boo = validate_password(list1[1])
    print(f"password validation = {boo}")
    print(f"list1 = {list1}")

def test1():
    request = Request(b'POST /dog.jpg?username=daveedas&password=123%21Password%23%21%40%23%24%25%5E%26%28%29%2D%5F%3D HTTP/1.1\r\n Host:       localhost:8080   \r\n   Connection:  keep-alive \r\n  headerasdiunasoudn:    asdasd \r\n   asodunasdheader2:asdoaisnd \r\n  header3forbettertesting:VALUE!!!\r\n   Cookie: id1    = thisdobeacookie; id2=   thisanothercookie; id3   =   thisathirdcookie\r\n\r\nHELLO WORLD!!!')
    extract_credentials(request)
    list1 = extract_credentials(request)
    boo = validate_password(list1[1])
    print(f"password validation = {boo}")
    print(f"list1 = {list1}")

def testidk():
    request = "https://duckduckgo.com/?q=web+development&ia=web&username=daveedas&password=1GenericPasscode!"
    list1 = extract_credentials(request)
    boo = validate_password(list1[1])
    print(f"password validation = {boo}")
    print(f"list1 = {list1}")


if __name__ == '__main__':
    test2()
   
 