from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    CategorySerializer,
    FoodCreateSerializer,
    FoodSerializer,
    OrderCreateSerializer,
    OrderSerializer,
)
from .models import Food, Category, Order
from .controllers import Delivery, Subtotal, Tax, Total

class FoodViews(APIView):
    def post(self, request):
        serializer = FoodCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        food = serializer.save()
        response_serializer = FoodSerializer(food)
        return Response(
            {"status": "success", "data": response_serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, id=None):
        if id is not None:
            item = get_object_or_404(Food, id=id)
            serializer = FoodSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Food.objects.all()
        serializer = FoodSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class CategoryViews(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id is not None:
            item = get_object_or_404(Category, id=id)
            serializer = CategorySerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Category.objects.all()
        serializer = CategorySerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class OrderViews(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, name=None):
        if name:
            item = Order.objects.filter(name__iexact=name)
            serializer = OrderSerializer(item, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Order.objects.all()
        serializer = OrderSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = serializer.save()
        response_serializer = OrderSerializer(order)
        return Response(
            {"status": "success", "data": response_serializer.data},
            status=status.HTTP_201_CREATED,
        )

class DeliveryView(APIView):
    def get(self, request, name=None, distance=0):
        items = Order.objects.filter(name__iexact=name)
        deliveryCost = Delivery.calculate(items,distance)
        return Response({"status": "success", "data": deliveryCost}, status=status.HTTP_200_OK)

class SubtotalView(APIView):
    def get(self, request, name=None, distance=0):
        items = Order.objects.filter(name__iexact=name)
        subtotal = Subtotal.calculate(items)
        return Response({"status": "success", "data": subtotal}, status=status.HTTP_200_OK)

class TaxView(APIView):
    def get(self, request, name=None, distance=0):
        items = Order.objects.filter(name__iexact=name)
        subtotal = Subtotal.calculate(items)
        deliveryCost = Delivery.calculate(items,distance)
        tax = Tax.calculate(subtotal, deliveryCost)
        return Response({"status": "success", "data": tax}, status=status.HTTP_200_OK)

class TotalView(APIView):
    def get(self, request, name=None, distance=0):
        items = Order.objects.filter(name__iexact=name)
        deliveryCost = Delivery.calculate(items,distance)
        total = Total.calculate(items, deliveryCost)
        return Response({"status": "success", "data": total}, status=status.HTTP_200_OK)