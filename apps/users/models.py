from django.db import models

# Create your models here.

class USer(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    mobile=models.CharField(max_length=11,unique=True)