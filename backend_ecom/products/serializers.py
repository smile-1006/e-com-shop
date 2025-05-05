from rest_framework import serializers
from .models import Product, CartManagement, OrderManagement, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartManagement
        fields = '__all__'

class OrderManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderManagement
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
