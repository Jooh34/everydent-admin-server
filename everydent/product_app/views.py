from datetime import datetime, timedelta

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Manufacturer, ProductInfo, Product
from .serializers import ManufacturerSerializer, ProductInfoSerializer, ProductSerializer

@api_view(['GET'])
def count_info(request):
    if request.method == 'GET':
        data = {
            'product_count': Product.objects.all().count(),
            'product_info_count': ProductInfo.objects.all().count(),
            'manufacturer_count': Manufacturer.objects.all().count(),
        }
        return Response(data)

@api_view(['GET'])
def expiry_list(request):
    THRESHOLD_DAYS = 2000
    if request.method == 'GET':
        time_threshold = datetime.now() + timedelta(days=THRESHOLD_DAYS)
        expiry_list = Product.objects.filter(expiry_end__lt=time_threshold)
        serializer = ProductSerializer(expiry_list, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def manufacturer_list(request):
    if request.method == 'GET':
        manu_list = Manufacturer.objects.all().order_by("id")
        serializer = ManufacturerSerializer(manu_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ManufacturerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def manufacturer_detail(request, pk):
    try:
        manu = Manufacturer.objects.get(pk=pk)
    except  Manufacturer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ManufacturerSerializer(manu)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ManufacturerSerializer(manu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        manu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def product_info_list(request):
    if request.method == 'GET':
        product_info_list = ProductInfo.objects.all().order_by("id")
        serializer = ProductInfoSerializer(product_info_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductInfoSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def product_info_detail(request, pk):
    if request.method == 'GET':
        product_info = ProductInfo.objects.get(pk=pk)
        serializer = ProductInfoSerializer(product_info)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # elif request.method == 'POST':
    #     serializer = ProductInfoSerializer(data=request.data)
    #
    #     try:
    #         product_info = ProductInfo()
    #         product_info.name = request.data['name']
    #         product_info.code = request.data['code']
    #         m_name = request.data['manufacturer_name']
    #         product_info.manufacturer = Manufacturer.objects.get(name=m_name)
    #         product_info.save()
    #         return Response({}, status=status.HTTP_201_CREATED)
    #
    #     except:
    #         return Response({}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def product_list(request):
    if request.method == 'GET':
        product_list = Product.objects.all().order_by("id")
        serializer = ProductSerializer(product_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        error_message = []

        stock_list = request.data
        for stock in stock_list:
            serializer = ProductSerializer(data=stock)
            if serializer.is_valid():
                serializer.save()
            else:
                error_message.append(serializer.errors)

        if len(error_message) == 0:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        # serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'DELETE':
        full_code = request.data.get('full_code', '')
        products = Product.objects.filter(full_code=full_code)
        if len(products) > 0:
            products[0].delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    print(request.method)
    if request.method == 'GET':
        print('why get?')
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        name = ProductInfo.objects.get(pk=product.product_info.id).name
        product.delete()
        return Response({'name': name}, status=status.HTTP_200_OK)



@api_view(['GET'])
def stock_list(request, product_info_id):
    try:
        product_info = ProductInfo.objects.get(id=product_info_id)
    except ProductInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    stock_list = Product.objects.filter(product_info=product_info)

    if request.method == 'GET':
        serializer = ProductSerializer(stock_list, many=True)
        return Response(serializer.data)
