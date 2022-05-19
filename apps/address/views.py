from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Address, Area
import json
from utils.view import LoginRequiredJSONMixin


# Create your views here.

#获取省份信息
class  ProvinceGetView(View):

    def get(self,request):
        try:
            provinces=Area.objects.filter(parent=None)

            provinces_list=[]

            for province in provinces:
                provinces_list.append({"id":province.id,"name":province.name})

        except Exception as e:
            return JsonResponse({"code":400,"errmsg":"Some errors with your database"})

        return JsonResponse({"code":0,"errmsg":"ok","province_list":provinces_list})


#获取区域信息
class  AreaGetView(View):

    def get(self,request,id):
        try:
            parent_name=Area.objects.get(id=id).name
            areas=Area.objects.filter(parent=id)
            areas_list=[]

            for area in areas:
                areas_list.append({"id":area.id,"name":area.name})

        except Exception as e:
            return JsonResponse({"code":400,"errmsg":"No children area data in database"})
        
        return JsonResponse({"code":0,"errmsg":"ok","sub_data":{"id":id,"area":parent_name,"subs":areas_list}})


class  AddressView(LoginRequiredJSONMixin,View):
    #地址新增
    def post(self,request):
        data = request.body.decode('utf-8')
        try:
            datajson = json.loads(data)
        except Exception as e:
            return JsonResponse({"code":400,"errmsg":"Inconrent json data"})
        user = request.user
        receiver = datajson.get('receiver')
        province_id=datajson.get('province_id')
        city_id=datajson.get('city_id')
        district_id=datajson.get('district_id')
        detail_address=datajson.get('detail_address')
        mobile=datajson.get('mobile')
        tel=datajson.get('tel')
        email=datajson.get('email')

        if not all([user,receiver,province_id,city_id,district_id,detail_address,mobile]):
            return JsonResponse({"code":400,"errmsg":"Incomplete parameters"})

        add = Address.objects.create(user=user,title = receiver,receiver=receiver,province=Area.objects.get(id=province_id),city=Area.objects.get(id=city_id),district=Area.objects.get(id=district_id),detail_address=detail_address,mobile=mobile,tel=tel,email=email)
        address ={
            'id':add.id,
            'title':add.title,
            'receiver':add.receiver,
            'province':add.province.name,
            'city':add.city.name,
            'district':add.district.name,
            'detail_address':add.detail_address,
            'mobile':add.mobile,
            'tel':add.tel,
            'email':add.email
        }
        return JsonResponse({'code':0,'errmsg':'ok','address':address})

    #地址获取
    def get(self,request):
        user = request.user
        addresses = Address.objects.filter(user = user,is_deleted=False)
        addresses_list=[]
        for add in addresses:
            addresses_list.append({
            'id':add.id,
            'title':add.title,
            'receiver':add.receiver,
            'province':add.province.name,
            'city':add.city.name,
            'district':add.district.name,
            'detail_address':add.detail_address,
            'mobile':add.mobile,
            'tel':add.tel,
            'email':add.email})
        return JsonResponse({'code':0,'errmsg':'ok','addresses':addresses_list})


    #地址删除
    def delete(self,request,id):

        user=request.user
        try:
            address=Address.objects.get(id=id)
        except Exception as e:
            return JsonResponse({"code":400,"errmsg":"Address is not exist"})

        if not address.user ==user:
            return JsonResponse({"code":400,"errmsg":"No permit"})

        address.delete()

        return JsonResponse({"code":0,"errmsg":"ok"})
        

    def put(self,request,id):
        data = request.body.decode('utf-8')
        try:
            datajson = json.loads(data)
        except Exception as e:
            return JsonResponse({"code":400,"errmsg":"Inconrent json data"})
        title = datajson.get('title')
        user =request.user
        try:
            address=Address.objects.get(id=id)
        except Exception as e:
            return JsonResponse({"code":400,"errmsg":"Address is not exist"})

        if not address.user ==user:
            return JsonResponse({"code":400,"errmsg":"No permit"})

        address.title=title
        address.save()
        print(str(address.title))
        return JsonResponse({"code":0,"errmsg":"ok"})

        
