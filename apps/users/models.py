from tabnanny import verbose
from django.db import models

# Create your models here.
#定义用户模型类
from django.contrib.auth.models import AbstractUser
class USer(AbstractUser):
    mobile=models.CharField(max_length=11,unique=True)

    class Meta:
        db_table = 'db_users'
        verbose_name='用户管理'
        verbose_name_plural=verbose_name

