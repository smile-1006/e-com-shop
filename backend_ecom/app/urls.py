# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import app, product_detail, send_otp, verify_otp, firstpage, signup, signin
from products.views import ProductViewSet, CartManagementViewSet, OrderManagementViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', CartManagementViewSet)
router.register(r'orders', OrderManagementViewSet)

urlpatterns = [
    path('', firstpage, name="firstpage"),
    path('home/', app, name="app"),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
]

urlpatterns += router.urls
urlpatterns += [
    path('<slug:slug>/', product_detail, name='product_detail'),
]
