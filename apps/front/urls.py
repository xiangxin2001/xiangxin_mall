from django.urls import path
from . import views

urlpatterns = [
    path('register',views.registerHtmlView),
    path('register.html',views.registerHtmlView),
    path('login',views.loginHtmlView),
    path('login.html',views.loginHtmlView),
    path('cart',views.cartHtmlView),
    path('cart.html',views.cartHtmlView),
    path('user_center_info',views.user_center_infoHtmlView),
    path('user_center_info.html',views.user_center_infoHtmlView),
    path('user_center_site',views.user_center_siteHtmlView),
    path('user_center_site.html',views.user_center_siteHtmlView),
    path('user_center_pass',views.user_center_passHtmlView),
    path('user_center_pass.html',views.user_center_passHtmlView),
    path('user_center_order',views.user_center_orderHtmlView),
    path('user_center_order.html',views.user_center_orderHtmlView),
    path('search',views.searchHtmlView),
    path('search.html',views.searchHtmlView),
    path('detail',views.detailHtmlView),
    path('detail.html',views.detailHtmlView),
    path('goods_judge',views.goods_judgeHtmlView),
    path('goods_judge.html',views.goods_judgeHtmlView),
    path('list',views.listHtmlView),
    path('list.html',views.listHtmlView),
    path('oauth_callback',views.oauth_callbackHtmlView),
    path('oauth_callback.html',views.oauth_callbackHtmlView),
]
