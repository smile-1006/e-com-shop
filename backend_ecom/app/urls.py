# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import app, product_detail
from products.views import ProductViewSet, CartManagementViewSet, OrderManagementViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', CartManagementViewSet)
router.register(r'orders', OrderManagementViewSet)

urlpatterns = [
    path('', app, name="app"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

urlpatterns += router.urls
urlpatterns += [
    path('<slug:slug>/', product_detail, name='product_detail'),
]
