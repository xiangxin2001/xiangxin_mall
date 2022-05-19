from django.db import models
# Create your models here.
#定义用户模型类
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    mobile=models.CharField(max_length=11,unique=True)
    default_address = models.ForeignKey('address.Address',related_name='user_address',null=True,blank=True,on_delete=models.SET_NULL,verbose_name='默认地址')
    class Meta:
        db_table = 'db_users'
        verbose_name='用户管理'
        verbose_name_plural=verbose_name

