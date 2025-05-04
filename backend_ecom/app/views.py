from django.shortcuts import render
from products.models import Product

# Create your views here.
def app(request):
    products = Product.objects.all() # Fetch all products
    
    context = {
        'products': products,
    } 
    return render(request, 'app.html', context)

# def first_page(request):
#     return render(request, 'first_page.html')

def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    context = { 'product': product }
    return render(request, 'product_detail.html', context)