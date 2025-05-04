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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderManagement.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))
        payment_mode = request.data.get('payment_mode')
        if not product_id or not payment_mode:
            return Response({'error': 'Product ID and payment mode are required'}, status=status.HTTP_400_BAD_REQUEST)
        order = OrderManagement.objects.create(
            user=request.user,
            product_id=product_id,
            quantity=quantity,
            price=0,  # Price can be set based on product price or other logic
            payment_mode=payment_mode
        )
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get_order_details(self, request, pk=None):
        try:
            order = self.get_object()
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        except OrderManagement.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        try:
            order = self.get_object()
            order.delete()
            return Response({'message': 'Order cancelled successfully'}, status=status.HTTP_204_NO_CONTENT)
        except OrderManagement.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
