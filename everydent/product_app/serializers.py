from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Manufacturer, ProductInfo

# 제조사 시리얼라이저
class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ("id", "name")

# 제품 정보 시리얼라이저
class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ("id", "name", "code", "manufacturer")
#
# # 제품 재고 추가 시리얼라이저
# class CreateProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("id", "username", "password")
#         extra_kwargs = {"password": {"write_only": True}}
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             validated_data["username"], None, validated_data["password"]
#         )
#         return user
