from django.urls import path
from . import views

urlpatterns = [
    path('areas/',views.ProvinceGetView.as_view()),
    path('areas/<id>/',views.AreaGetView.as_view()),
    path('addresses/create/',views.AddressView.as_view()),
    path('addresses/',views.AddressView.as_view()),
    path('addresses/<id>/',views.AddressView.as_view()),
    path('addresses/<id>/title/',views.AddressView.as_view()),
]
