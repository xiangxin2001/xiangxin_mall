
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

    def get(self,request):
        # 判断用户是否登录
        user=request.user
        if user.is_authenticated:

            # 登录用户查询redis
            redis_cli=get_redis_connection('carts')
            sku_id_counts=redis_cli.hgetall('carts_%s'%user.id)
            selected_ids=redis_cli.smembers('selected_%s'%user.id)

            carts={}

            for sku_id,count in sku_id_counts.items():
                carts[int(sku_id)]={
                    'count':int(count),
                    'selected': sku_id in selected_ids
                }
        else:
            # 未登录用户查询cookie
            cookie_carts=request.COOKIES.get('carts')
            if cookie_carts is not None:
               carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
                carts={}


        sku_ids=carts.keys()

        skus=SKU.objects.filter(id__in=sku_ids)
        sku_list=[]
        for sku in skus:
            # 将对象数据转换为字典数据
            sku_list.append({
                'id':sku.id,
                'price':sku.price,
                'name':sku.name,
                'default_image_url':sku.default_image.url,
                'selected': carts[sku.id]['selected'],          
                'count': int(carts[sku.id]['count']),                
                'amount': sku.price*carts[sku.id]['count']     
            })
        # 6 返回响应
        return Response({'code':0,'errmsg':'ok','cart_skus':sku_list})


    def put(self,request):
            user=request.user
            # 2.接收数据
            data=request.data
            sku_id=data.get('sku_id')
            count=data.get('count')
            selected=data.get('selected')
            # 3.验证数据
            if not all([sku_id,count]):
                return Response({'code':400,'errmsg':'参数不全'})

            try:
                SKU.objects.get(id=sku_id)
            except SKU.DoesNotExist:
                return Response({'code':400,'errmsg':'没有此商品'})

            try:
                count=int(count)
            except Exception:
                count=1

            if user.is_authenticated:

                redis_cli=get_redis_connection('carts')
      
                redis_cli.hset('carts_%s'%user.id,sku_id,count)
  
                if selected:
                    redis_cli.sadd('selected_%s'%user.id,sku_id)
                else:
                    redis_cli.srem('selected_%s'%user.id,sku_id)
       
                return Response({'code':0,'errmsg':'ok','cart_sku':{'count':count,'selected':selected}})

            else:
 
                cookie_cart=request.COOKIES.get('carts')
     
                if cookie_cart is not None:
 
                    carts=pickle.loads(base64.b64decode(cookie_cart))
                else:

                    carts={}

                if sku_id in carts:
                    carts[sku_id]={
                        'count':count,
                        'selected':selected
                    }
                
                new_carts=base64.b64encode(pickle.dumps(carts))

                return Response({'code':0,'errmsg':'ok','cart_sku':{'count':count,'selected':selected}}).set_cookie('carts',new_carts.decode(),max_age=14*24*3600)

   
    def delete(self,request):

        data=request.data
        sku_id=data.get('sku_id')
        try:
            SKU.objects.get(pk=sku_id)  # pk primary key
        except SKU.DoesNotExist:
            return Response({'code':400,'errmsg':'没有此商品'})
        user=request.user
        if user.is_authenticated:

            redis_cli=get_redis_connection('carts')

            redis_cli.hdel('carts_%s'%user.id,sku_id)
            redis_cli.srem('selected_%s'%user.id,sku_id)
            return Response({'code':0,'errmsg':'ok'})

        else:
            cookie_cart=request.COOKIES.get('carts')
            #  判断数据是否存在
            if cookie_cart is not None:

                carts=pickle.loads(base64.b64decode(cookie_cart))
            else:

                carts={}
            # 删除数据 
            del carts[sku_id]
         
            new_carts=base64.b64encode(pickle.dumps(carts))

            return Response({'code':0,'errmsg':'ok'}).set_cookie('carts',new_carts.decode(),max_age=14*24*3600)
    


