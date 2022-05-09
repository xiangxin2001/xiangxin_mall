from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import User
from django.views import View


class UsernameCountView(View):

    def get(self,request,username):


        count = User.objects.filter(username=username).count()
        return JsonResponse({'code':0,'count':count,'err':'ok'})
