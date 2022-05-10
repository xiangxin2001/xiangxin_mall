
from django.shortcuts import render
from django.views import View

def registerView(request):
    return render(request,'register.html')

def loginView(request):
    return render(request,'login.html')

def indexView(request):
    return render(request,'index.html')