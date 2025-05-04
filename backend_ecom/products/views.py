from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, CartManagement, OrderManagement
from .serializers import ProductSerializer, CartManagementSerializer, OrderManagementSerializer

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['product_name']
    ordering_fields = ['price']
    filterset_fields = ['category__category_name', 'sold', 'price']

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class CartManagementViewSet(viewsets.ModelViewSet):
    queryset = CartManagement.objects.all()
    serializer_class = CartManagementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartManagement.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        cart_item, created = CartManagement.objects.get_or_create(user=request.user, product_id=product_id)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def increase_quantity(self, request, pk=None):
        cart_item = self.get_object()
        cart_item.quantity += 1
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def decrease_quantity(self, request, pk=None):
        cart_item = self.get_object()
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data)
        else:
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['delete'])
    def remove_from_cart(self, request, pk=None):
        cart_item = self.get_object()
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderManagementViewSet(viewsets.ModelViewSet):
    queryset = OrderManagement.objects.all()
    serializer_class = OrderManagementSerializer
