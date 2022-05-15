from django.urls import path
from . import views

urlpatterns = [
    path('register',views.registerHtmlView),
    path('register.html',views.registerHtmlView),
    path('login',views.loginHtmlView),
    path('login.html',views.loginHtmlView),
    path('',views.indexHtmlView),
    path('index.html',views.indexHtmlView),
    path('cart',views.cartHtmlView),
    path('cart.html',views.cartHtmlView),
    path('user_center_info',views.user_center_infoHtmlView),
    path('user_center_info.html',views.user_center_infoHtmlView),
    
]
