
from django.shortcuts import render
from django.views import View

def registerHtmlView(request):
    return render(request,'register.html')

def loginHtmlView(request):
    return render(request,'login.html')

def indexHtmlView(request):
    return render(request,'index.html')

def cartHtmlView(request):
    return render(request,'cart.html')

def user_center_infoHtmlView(request):
    return render(request,'user_center_info.html')