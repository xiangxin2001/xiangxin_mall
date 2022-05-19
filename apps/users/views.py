import json
import re
from django.http import JsonResponse


from apps.front import views
from django.contrib.auth import login,authenticate,logout
from utils.view import LoginRequiredJSONMixin
# Create your views here.
from .models import User
from django.views import View

#检查用户名是否已存在
class usernameCountAPI(View):

    def get(self,request,username):


        count = User.objects.filter(username=username).count()
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})

#检查手机号是否已存在
class mobileCountAPI(View):
    def get(self,request,mobile):

        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})

#新用户注册API
class registerNewAPI(View):
    def post(self,request):
        data=request.body.decode('utf-8')
        try:
            user=json.loads(data)
        except Exception as e:
            return JsonResponse({"code":400,"errmsg":"Inconrent json data"})
        username=user.get('username')
        password=user.get('password')
        password2=user.get('password2')
        mobile=user.get('mobile')
        allow=user.get('allow')

        if not all([username,password,password2,mobile,allow]):
            return JsonResponse({'code':400,'errmsg':'Incomplete parameters'})

        if not re.match('[a-zA-Z0-9_-]{5,20}',username):
            return JsonResponse({'code':400,'errmsg':'Incorrect user name'})
        
        if not password==password2:
            return JsonResponse({'code':400,'errmsg':'Password error'})

        if not re.match('1[345789]\d{9}',mobile):
            return JsonResponse({'code':400,'errmsg':'Incorrect mobilephone number'})

        if not 8<=len(password)<=20:
            return JsonResponse({'code':400,'errmsg':'Incorrect password length'})

        if not allow:
            return JsonResponse({'code':400,'errmsg':'Agreement not agreed'})

        #保存用户注册信息到数据库
        user_save=User.objects.create_user(username=username,password=password,mobile=mobile)

        login(request,user_save)

        return JsonResponse({'code':0,'errmsg':'ok'})

#用户登录API
class userloginAPI(View):
    def post(self,request):
        try:
            data=json.loads(request.body.decode())
        except Exception as e:
            return JsonResponse({"code":400,"errmsg":"Inconrent json data"})
        username=data.get('username')
        password=data.get('password')
        remembered=data.get('remembered')

        if not all([username,password]):
            return JsonResponse({'code':400,'errmsg':'Incomplete parameters'})

        
        #判断是否是手机号登录
        if re.match('1[345789]\d{9}',username):
            User.USERNAME_FIELD='mobile'
        else:
            User.USERNAME_FIELD='username'
        
        #登录验证
        user=authenticate(username=username,password=password)
        if not user:
            return JsonResponse({'code':400,'errmsg':'Incorrect user name or password'})

        
        #是否登录保持
        if remembered:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        
        login(request,user)

        #获取登录用户信息
        a=object()
        if User.USERNAME_FIELD=='mobile':
            a=User.objects.get(mobile=username)
        else:
            a=User.objects.get(username=username)

        #制作响应信息
        response=JsonResponse({'code':0,'errmsg':'ok'})
        response.set_cookie('username',a.username)

        return response

#用户退出API
class logoutAPI(View):
    def delete(self,request):
        logout(request)

        response=JsonResponse({'code':0,'errmsg':'ok'})
        response.delete_cookie('username')

        return response


#用户中心进入API
class centerViewAPI(LoginRequiredJSONMixin,View):

    def get(self,request):
        user=request.user

        info={
            'username':user.username,
            'mobile':user.mobile
        }


        return JsonResponse({'code':0,'errmsg':'ok','info_data':info})


#用户修改密码
class passwordChangeAPI(View):
    def put(self,request):
        user=request.user
        data = request.body.decode('utf-8')
        try:
            datajson = json.loads(data)
        except Exception as e:
            return JsonResponse({"code":400,"errmsg":"Inconrent json data"})
        old_password=datajson.get('old_password')
        new_password=datajson.get('new_password')
        new_cpassword=datajson.get('new_password2')
        if not user.check_password(old_password):
            return JsonResponse({"code":400,"errmsg":"Inconrent password"})
        if new_cpassword!=new_password:
            return JsonResponse({"code":400,"errmsg":"Inconrent data"})

        user.set_password(new_password)
        user.save()

        return JsonResponse({'code':0,'errmsg':'ok'})


