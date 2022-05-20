
from django.shortcuts import render
from django.views import View
from django.middleware.csrf import get_token

def registerHtmlView(request):
    return render(request,'register.html')

def loginHtmlView(request):
    return render(request,'login.html')

def indexHtmlView(request):
    get_token(request)
    return render(request,'index.html')

def user_center_infoHtmlView(request):
    return render(request,'user_center_info.html')

def user_center_siteHtmlView(request):
    return render(request,'user_center_site.html')

def user_center_passHtmlView(request):
    return render(request,'user_center_pass.html')

def user_center_orderHtmlView(request):
    return render(request,'user_center_order.html')

def searchHtmlView(request):
    return render(request,'search.html')

def cartHtmlView(request):
    return render(request,'cart.html')

def detailHtmlView(request):
    return render(request,'detail.html')

def goods_judgeHtmlView(request):
    return render(request,'goods_judge.html')

def listHtmlView(request):
    return render(request,'list.html')

def oauth_callbackHtmlView(request):
    return render(request,'oauth_callback.html')
