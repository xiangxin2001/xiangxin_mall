from django.urls import path
from . import views

urlpatterns = [
    path('usernames/<username:username>/count/',views.usernameCountAPI.as_view()),
    path('register/new/',views.registerNewAPI.as_view()),
    path('mobiles/<mobile:mobile>/count/',views.mobileCountAPI.as_view()),
    path('login/userlogin/',views.userloginAPI.as_view()),
    path('logout/',views.logoutAPI.as_view()),
]
