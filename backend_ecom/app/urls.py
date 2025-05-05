# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import app, product_detail, send_otp, verify_otp, firstpage, signup, signin, current_date, get_cart, add_to_cart, increase_quantity, decrease_quantity, remove_from_cart, place_order, get_orders, cancel_order
from products.views import ProductViewSet, CartManagementViewSet, OrderManagementViewSet, CategoryListView

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
    path('current-date/', current_date, name='current_date'),
    path('cart/', get_cart, name='get_cart'),
    path('cart/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/<int:cart_item_id>/increase_quantity/', increase_quantity, name='increase_quantity'),
    path('cart/<int:cart_item_id>/decrease_quantity/', decrease_quantity, name='decrease_quantity'),
    path('cart/<int:cart_item_id>/remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    # Order URLs
    path('orders/place_order/', place_order, name='place_order'),
    path('orders/', get_orders, name='get_orders'),
    path('orders/<int:order_id>/cancel_order/', cancel_order, name='cancel_order'),
    path('categories/', CategoryListView.as_view(), name='categories'),
]

urlpatterns += router.urls
urlpatterns += [
    path('<slug:slug>/', product_detail, name='product_detail'),
]
