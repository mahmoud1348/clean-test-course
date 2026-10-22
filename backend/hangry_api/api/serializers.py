from rest_framework import serializers
from .models import Food, Category, Order


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=225)
    description = serializers.CharField(max_length=225)

    class Meta:
        model = Category
        fields = ('__all__')

class FoodSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=225)
    price = serializers.FloatField()
    description = serializers.CharField(max_length=225)
    category = serializers.StringRelatedField()

    class Meta:
        model = Food
        fields = ('__all__')


class FoodCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Food
        fields = ('name', 'price', 'description', 'category')


class OrderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=225)
    item = serializers.StringRelatedField()
    quantity = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ('__all__')


class OrderCreateSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Order
        fields = ('name', 'item', 'quantity')