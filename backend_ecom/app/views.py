from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import now
from products.models import Product, Category
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
import random
import time
from django.conf import settings
from twilio.rest import Client

# In-memory store for OTPs: {mobile: (otp, expiry_timestamp)}
otp_store = {}

User = get_user_model()

def app(request):
    products = Product.objects.all() # Fetch all products
    
    context = {
        'products': products,
    } 
    return render(request, 'app.html', context)

def firstpage(request):
    category = request.GET.get('category')
    sold = request.GET.get('sold')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    search = request.GET.get('search')

    products = Product.objects.all()

    if category:
        products = products.filter(category__category_name=category)
    if sold in ['true', 'false']:
        products = products.filter(sold=(sold == 'true'))
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    if search:
        products = products.filter(product_name__icontains=search)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'sold': sold,
        'price_min': price_min,
        'price_max': price_max,
        'search': search,
    }
    return render(request, 'firstpage.html', context)

def signup(request):
    return render(request, 'signup.html')

def signin(request):
    return render(request, 'signin.html')

from django.http import Http404

def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    context = { 'product': product }
    return render(request, 'product_detail.html', context)

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        if not mobile:
            return JsonResponse({'error': 'Mobile number is required'}, status=400)
        otp = str(random.randint(100000, 999999))
        expiry = time.time() + 300  # OTP valid for 5 minutes
        otp_store[mobile] = (otp, expiry)
        # Send OTP via Twilio SMS
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your OTP is {otp}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=mobile
            )
        except Exception as e:
            return JsonResponse({'error': f'Failed to send OTP: {str(e)}'}, status=500)
        return JsonResponse({'message': 'OTP sent successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        otp = request.POST.get('otp')
        if not mobile or not otp:
            return JsonResponse({'error': 'Mobile and OTP are required'}, status=400)
        stored_otp, expiry = otp_store.get(mobile, (None, None))
        if stored_otp is None:
            return JsonResponse({'error': 'OTP not found. Please request a new one.'}, status=400)
        if time.time() > expiry:
            del otp_store[mobile]
            return JsonResponse({'error': 'OTP expired. Please request a new one.'}, status=400)
        if otp != stored_otp:
            return JsonResponse({'error': 'Invalid OTP'}, status=400)
        # OTP is valid, authenticate or create user
        user, created = User.objects.get_or_create(mobile=mobile)
        # Log the user in (session-based)
        login(request, user)
        del otp_store[mobile]
        return JsonResponse({'message': 'OTP verified, user logged in', 'user': {'mobile': user.mobile, 'full_name': user.full_name}})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def current_date(request):
    from django.utils.timezone import now
    return JsonResponse({'date': now().strftime('%Y-%m-%d')})
