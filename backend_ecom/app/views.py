from django.shortcuts import render
from products.models import Product

# Create your views here.
def app(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'app.html', {'products': products})