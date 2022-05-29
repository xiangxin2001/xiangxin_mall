import pickle
import base64

from django_redis import get_redis_connection


def merge_cookie_to_redis(request,response):

    cookie_carts = request.COOKIES.get('carts')

    if cookie_carts is not None:
        carts=pickle.loads(base64.b64decode(cookie_carts))

        
        cookie_dict={}

        selected_ids=[]
        #  初始化一个列表 用于保存未选中的商品id
        unselected_ids=[]

        # 遍历cookie数据
        for sku_id,count_selected_dict in carts.items():
       
            cookie_dict[sku_id]=count_selected_dict['count']
            if count_selected_dict['selected']:
                selected_ids.append(sku_id)
            else:
                unselected_ids.append(sku_id)
        user=request.user

        redis_cli=get_redis_connection('carts')
        pipeline=redis_cli.pipeline()
        pipeline.hmset('carts_%s'%user.id,cookie_dict)
        if len(selected_ids)>0:
            pipeline.sadd('selected_%s'%user.id,*selected_ids)

        if len(unselected_ids)>0:
            pipeline.srem('selected_%s'%user.id,*unselected_ids)

        pipeline.execute()
        response.delete_cookie('carts')

    return response