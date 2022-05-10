import json
import re
from click import password_option
from django.http import JsonResponse
from django.shortcuts import render
from matplotlib.pyplot import cla
from soupsieve import match

from apps.front import views

# Create your views here.
from .models import User
from django.views import View


class usernameCountView(View):

    def get(self,request,username):


        count = User.objects.filter(username=username).count()
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})


class mobileCountView(View):
    def get(self,request,mobile):

        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})


class registerNewView(View):
    def post(self,request):
        data=request.body.decode('utf-8')
        user=json.loads(data)
        username=user.get('username')
        password=user.get('password')
        password2=user.get('password2')
        mobile=user.get('mobile')
        allow=user.get('allow')

        if not all(username,password,password2,mobile,allow):
            return JsonResponse({'code':400,'errmsg':'Incomplete parameters'})

        if not re.match('[a-zA-Z0-9_-]{5,20}',username):
            return JsonResponse({'code':400,'errmsg':'Incorrect user name'})
        
        if not password==password2:
            return JsonResponse({'code':400,'errmsg':'Password error'})

        if not re.match('1[345789]\d{9}',mobile):
            return JsonResponse({'code':400,'errmsg':'Incorrect mobilephone number'})

        if not 8<len(password)<20:
            return JsonResponse({'code':400,'errmsg':'Incorrect password length'})

        if not allow:
            return JsonResponse({'code':400,'errmsg':'Agreement not agreed'})



        return JsonResponse({'code':0,'errmsg':'ok'})
