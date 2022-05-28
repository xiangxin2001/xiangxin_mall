import json

from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from django_redis import get_redis_connection
from apps.goods.models import SKU
import pickle
import base64

class CartsView(APIView):

    
    def post(self,request):
        # 接收数据
        data=request.data
        sku_id=data.get('sku_id')
        count=data.get('count')
        # 验证数据

        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return Response({'code':400,'errmsg':'查无此商品'})


        try:
            count=int(count)
        except Exception:
            count=1
        # 判断用户的登录状态
        user=request.user
        if user.is_authenticated:
           
            redis_cli=get_redis_connection('carts')
            
            redis_cli.hset('carts_%s'%user.id,sku_id,count)
            
            redis_cli.sadd('selected_%s'%user.id,sku_id)
            return Response({'code':0,'errmsg':'ok'})
        else:
           
            cookie_carts=request.COOKIES.get('carts')
            if cookie_carts:
               
                carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
               
                carts={}

            # 判断新增的商品 有没有在购物车里
            if sku_id in carts:
    
                origin_count=carts[sku_id]['count']
                count+=origin_count

            carts[sku_id]={
                'count':count,
                'selected':True
            }




            carts_bytes=pickle.dumps(carts)
     

            base64encode=base64.b64encode(carts_bytes)

            return Response({'code': 0, 'errmsg': 'ok'}).set_cookie('carts',base64encode.decode(),max_age=3600*24*12)

