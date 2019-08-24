from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Manufacturer, ProductInfo, Product

class ManufacturerSerializer(serializers.ModelSerializer):
    product_info_count = serializers.SerializerMethodField()

    def get_product_info_count(self, obj):
        return ProductInfo.objects.filter(manufacturer=obj).count()

    class Meta:
        model = Manufacturer
        fields = ("id", "name", "code", "product_info_count")

class ProductInfoSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.CharField(source='manufacturer.name')
    product_count = serializers.SerializerMethodField()

    def get_product_count(self, obj):
        return Product.objects.filter(product_info=obj).count()

    class Meta:
        model = ProductInfo
        fields = ("id", "name", "code", "manufacturer", "manufacturer_name", "product_count")

# 제품 재고 시리얼라이저
class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('_user')
    name = serializers.SerializerMethodField()
    manufacturer_name = serializers.SerializerMethodField()
    expiry_start = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', 'iso-8601'])
    expiry_end = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d', 'iso-8601'])

    def _user(self, obj):
        request = getattr(self.context, 'request', None)
        if request:
            if request.user:
                return request.user
            else:
                return None

    def get_name(self, obj):
        return obj.product_info.name

    def get_manufacturer_name(self, obj):
        return obj.product_info.manufacturer.name

    class Meta:
        model = Product
        fields = ("id", "created_time", "product_info", "full_code", "owner", "expiry_start", "expiry_end", "name", "manufacturer_name")
