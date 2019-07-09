from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Manufacturer, ProductInfo
from .serializers import ManufacturerSerializer, ProductInfoSerializer

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
