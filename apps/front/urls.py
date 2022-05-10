from django.urls import path
from . import views

urlpatterns = [
    path('register',views.registerView),
    path('register.html',views.registerView),
    path('login',views.loginView),
    path('login.html',views.loginView),
    path('',views.indexView),
    path('index.html',views.indexView),
    
]
