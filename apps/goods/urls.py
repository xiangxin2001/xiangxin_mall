from django.urls import path
from . import views

urlpatterns = [
    path('',views.IndexView.as_view()),
    path('index.html',views.IndexView.as_view()),
    path('list/<category_id>/skus/',views.ListView.as_view())
]
