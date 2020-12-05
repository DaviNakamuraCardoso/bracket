from .models import User 
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

def register_user(request, c):
    """
    Handles the register of an user
    :param c: form cleaned data
    """
    password = c['password']
    confirmation = c['confirmation']

    if password != confirmation: 
        return False 

    else: 
        try: 
            user = User(
                password=password, 
                username=get_username(c), 
                first_name=c['first_name'], 
                last_name=c['last_name'], 
                email=c['email'], 
                birth=c['birth'],
                trade_number=str(c['trade_number'])
            )
            user.save()
            login(request, user)
            return True 

        except IntegrityError: 
            return False 

    return True 

def login_user(request, c): 
    """
    :param: c => Form input
    Deals with the login, returning True for successful process and False for failure
    """
    key = c['key']
    password = c['password']
    if "@" in key: 
        user = authenticate(request, email=key, password=password)

    else: 
        user = authenticate(request, username=key, password=password)
    
    if user is not None: 
        login(request, user)
    else: 
        return False 
    
    return True 


def get_username(c):
    """
    :param: c -> Form cleaned data 
    Defines a username based on first and last name 
    """
    first = str(c['first_name'])
    last = str(c['last_name'])
    sep = ""

    equal_users = len(User.objects.all().filter(first_name=first, last_name=last))
    return f'{sep.join(first.lower().split())}.{sep.join(last.lower().split())}.{"{:0>2d}".format(equal_users+1)}'
