from datetime import datetime, timedelta
from django.db.models import Q, Count

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Manufacturer, ProductInfo, Product
from .serializers import ManufacturerSerializer, ProductInfoSerializer, ProductSerializer

import re

@api_view(['GET'])
def count_info(request):
    if request.method == 'GET':
        result = []
        for productinfo in ProductInfo.objects.all():
            # check duplication
            if productinfo.name in result:
                pass
            else:
                result.append(productinfo.name,)


        data = {
            'product_count': Product.objects.filter(status=1).count(),
            'product_info_count': len(result),
            'manufacturer_count': Manufacturer.objects.all().count(),
        }
        return Response(data)

@api_view(['GET'])
def expiry_list(request):
    THRESHOLD_DAYS = 100
    if request.method == 'GET':
        time_threshold = datetime.now() + timedelta(days=THRESHOLD_DAYS)
        expiry_list = Product.objects.filter(status=1, expiry_end__lt=time_threshold).order_by('expiry_end')
        serializer = ProductSerializer(expiry_list, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def running_out_list(request):
    def is_name_exist(name, list):
        for el in list:
            if name == el['name']:
                return True
        return False

    THRESHOLD_COUNTS = 5
    if request.method == 'GET':
        result = []
        product_info_list = ProductInfo.objects.all()
        #product_info_list = ProductInfo.objects.all().annotate(num_product=Count('product_set', filter=Q(product_set__status=1))).order_by('num_product')
        for productinfo in product_info_list:
            if productinfo.product_set.count() <= THRESHOLD_COUNTS:
                # count all same name of p_i
                pi_list = ProductInfo.objects.filter(name=productinfo.name)
                sum = 0
                for pi in pi_list:
                    sum = sum + Product.objects.filter(status=1, product_info=pi).count()

                # check sum
                if sum <= THRESHOLD_COUNTS:
                    # check duplication
                    if is_name_exist(productinfo.name, result):
                        pass
                    else:
                        result.append({
                            'name' : productinfo.name,
                            'manufacturer_name' : productinfo.manufacturer.name,
                            'product_total_count' : sum,
                        })

        result = sorted(result, key=lambda pi: pi['product_total_count'])
        return Response(result)

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
    def is_name_exist(name, list):
        for el in list:
            if name == el['name']:
                return True
        return False

    if request.method == 'GET':
        result = []

        product_info_list = ProductInfo.objects.all().order_by("name")
        convert = lambda text: int(text) if text.isdigit() else text
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key.name) ]
        product_info_list = sorted( product_info_list, key=alphanum_key )

        for productinfo in product_info_list:
            # count all same name of p_i
            pi_list = ProductInfo.objects.filter(name=productinfo.name)
            product_sum = 0
            returned_sum = 0
            for pi in pi_list:
                product_sum = product_sum + Product.objects.filter(status=1, product_info=pi).count()
                returned_sum = returned_sum + Product.objects.filter(status=3, product_info=pi).count()

            # check duplication
            if is_name_exist(productinfo.name, result):
                pass
            else:
                result.append({
                    'id' : productinfo.id,
                    'name' : productinfo.name,
                    'code' : productinfo.code,
                    'manufacturer' : productinfo.manufacturer.id,
                    'manufacturer_name' : productinfo.manufacturer.name,
                    'product_total_count' : product_sum,
                    'returned_total_count' : returned_sum,
                })

        return Response(result)

    elif request.method == 'POST':
        if request.data.get('manufacturer', None) is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductInfoSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def product_info_detail(request, pk):
    if request.method == 'GET':
        product_info = ProductInfo.objects.get(pk=pk)
        serializer = ProductInfoSerializer(product_info)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        product_info = ProductInfo.objects.get(pk=pk)
        pi_list = ProductInfo.objects.filter(name=product_info.name)
        for pi in pi_list:
            pi.delete()

        return Response({'name': product_info.name}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        new_name = request.data['name']
        product_info = ProductInfo.objects.get(pk=pk)
        pi_list = ProductInfo.objects.filter(name=product_info.name)
        for pi in pi_list:
            pi.name = new_name
            pi.save()

        return Response(status=status.HTTP_200_OK)

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
def product_info_all_list(request):
    if request.method == 'GET':
        pi_list = ProductInfo.objects.all()
        serializer = ProductInfoSerializer(pi_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def product_list(request):
    if request.method == 'GET':
        product_list = Product.objects.filter(status=1).order_by("id")
        serializer = ProductSerializer(product_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        error_message = []

        stock_list = request.data
        for stock in stock_list:
            serializer = ProductSerializer(data=stock, partial=True)
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

@api_view(['POST'])
def product_status_list(request):
    if request.method == 'POST':
        error_message = []

        stock_list = request.data['list']
        new_status = request.data['status']

        for i, stock in enumerate(stock_list):
            full_code = stock['full_code']
            products = Product.objects.filter(status=1, full_code=full_code.strip())
            if len(products) > 0:
                product = products[0]
                new_status = request.data['status']
                product.status = new_status
                product.save()
            else:
                error_message.append('{}번째 : {} 은 재고목록에 존재하지 않아 처리되지 않았습니다.\n'.format(i+1, stock['name']))

        print(error_message)
        if len(error_message) == 0:
            return Response(status=status.HTTP_200_OK)
        else:
            print(error_message)
            print('\n'.join(error_message))
            return Response({'error_message' : '\n'.join(error_message)}, status=status.HTTP_200_OK)

@api_view(['POST'])
def product_status_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        new_status = request.data['status']
        product.status = new_status
        product.save()
        return Response({'name': product.product_info.name}, status=status.HTTP_200_OK)

@api_view(['GET'])
def stock_list(request, product_info_id):
    try:
        product_info = ProductInfo.objects.get(id=product_info_id)
    except ProductInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # get all same name product_infos
        pi_list = ProductInfo.objects.filter(name=product_info.name)
        queryset_sum = Product.objects.none()
        for pi in pi_list:
            queryset_sum |= Product.objects.filter(status=1, product_info=pi)

        serializer = ProductSerializer(queryset_sum, many=True)
        return Response(serializer.data)
