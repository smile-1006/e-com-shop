from django.contrib import admin

# Register your models here.
from .models import Product, Category, CartManagement, OrderManagement

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartManagement)
admin.site.register(OrderManagement)