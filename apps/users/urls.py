from django.urls import path
from . import views

urlpatterns = [
    path('usernames/<username:username>/count/',views.usernameCountView.as_view()),
    path('register/new/',views.registerNewView.as_view()),
    path('mobiles/<mobile:mobile>/count/',views.mobileCountView.as_view())
]
