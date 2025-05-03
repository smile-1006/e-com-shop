from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Product, CartManagement, OrderManagement
from .serializers import ProductSerializer, CartManagementSerializer, OrderManagementSerializer

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_name']
    ordering_fields = ['price']

class CartManagementViewSet(viewsets.ModelViewSet):
    queryset = CartManagement.objects.all()
    serializer_class = CartManagementSerializer

class OrderManagementViewSet(viewsets.ModelViewSet):
    queryset = OrderManagement.objects.all()
    serializer_class = OrderManagementSerializer
