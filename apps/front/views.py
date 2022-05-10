
from django.shortcuts import render
from django.views import View

def RegisterView(request):
    return render(request,'register.html')