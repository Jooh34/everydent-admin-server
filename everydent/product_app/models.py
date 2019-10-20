from django.db import models
from django.contrib.auth.models import User

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

class ProductInfo(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, related_name='product_infos', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)

class Product(models.Model):
    created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    product_info = models.ForeignKey(ProductInfo, related_name='product_set', on_delete=models.CASCADE)
    full_code = models.CharField(max_length=100, default='')
    owner = models.ForeignKey(User, related_name="owners", on_delete=models.SET_NULL, null=True)
    expiry_start = models.DateField(null=True)
    expiry_end = models.DateField(null=True)
    STATUS_CHOICES = (
        (1, '보유'),
        (2, '삭제'),
        (3, '반품'),
    )
    status = models.IntegerField(default=1, choices=STATUS_CHOICES)
    status_edit_date = models.DateTimeField(null=True)
