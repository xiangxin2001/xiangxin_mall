from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from utils.goods import get_categories
from apps.contents.models import ContentCategory
from apps.goods.models import GoodsCategory
from rest_framework.response import Response
from utils.goods import get_breadcrumb
from apps.goods.models import SKU
from utils.goods import get_goods_specs
from haystack.views import SearchView
from django.http import JsonResponse

#主页视图
class IndexView(APIView):

    def get(self,request):
        # 1.商品分类数据
        categories=get_categories()
        # 2.广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request,'index.html',context)


#分类商品列表视图
class ListView(APIView):

    def get(self,request,category_id):
        # 每页多少条数据
        ordering=request.GET.get('ordering')
        # 要第几页数据
        page_size=request.GET.get('page_size')
        # 获取分类id,根据分类id进行分类数据的查询验证
        page=request.GET.get('page')

        
        try:
            category=GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return Response({'code':400,'errmsg':'参数缺失'})
        
        breadcrumb=get_breadcrumb(category)

        # 查询分类对应的sku数据，然后排序，然后分页
        skus=SKU.objects.filter(category=category,is_launched=True).order_by(ordering)
        from django.core.paginator import Paginator
        paginator=Paginator(skus,per_page=page_size)

        page_skus=paginator.page(page)

        sku_list=[]
        for sku in page_skus.object_list:
            sku_list.append({
                'id':sku.id,
                'name':sku.name,
                'price':sku.price,
                'default_image_url':sku.default_image.url
            })

        # 获取总页码
        total_num = paginator.num_pages
        return Response({'code':0,'errmsg':'ok','list':sku_list,'count':total_num,'breadcrumb':breadcrumb})


class SKUSearchView(SearchView):

    def create_response(self):
        # 获取搜索的结果
        context = self.get_context()
        sku_list=[]
        for sku in context['page'].object_list:
            sku_list.append({
                'id':sku.object.id,
                'name':sku.object.name,
                'price': sku.object.price,
                'default_image_url': sku.object.default_image.url,
                'searchkey': context.get('query'),
                'page_size': context['page'].paginator.num_pages,
                'count': context['page'].paginator.count
            })

        return JsonResponse(sku_list,safe=False)




class DetailView(APIView):
    #商品详情页
    def get(self,request,sku_id):
        try:
            sku=SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return Response({"code":404,"errmag":"not exist"},status=404)

        categories=get_categories()
        
        breadcrumb=get_breadcrumb(sku.category)
  
        goods_specs=get_goods_specs(sku)

        context = {

            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs': goods_specs,
            

        }
        return render(request,'detail.html',context)
