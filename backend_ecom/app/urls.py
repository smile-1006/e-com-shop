from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from products.views import ProductViewSet, CartManagementViewSet, OrderManagementViewSet

urlpatterns = [
    path('', app, name="app"),  # Include the app's URLs under the 'api/' prefix
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', CartManagementViewSet)
router.register(r'orders', OrderManagementViewSet)

urlpatterns += router.urls