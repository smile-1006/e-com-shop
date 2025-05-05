from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.timezone import now
from products.models import Product, Category, OrderManagement as Order, OrderItem
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model, login
import random
import time
import json
from django.conf import settings
from twilio.rest import Client
from django.utils import timezone

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
        # Format mobile number to E.164 if not already
        if not mobile.startswith('+'):
            mobile = '+91' + mobile  # Assuming India country code
        otp = str(random.randint(100000, 999999))
        expiry = time.time() + 300  # OTP valid for 5 minutes
        otp_store[mobile] = (otp, expiry)
        # Send OTP via Twilio SMS
        try:
            client = Client('AC1693f9872f947400100704ad4756a746', '7f4f6a3d3cdaf022e284a1273b02e9ad')
            message = client.messages.create(
                body=f"Your OTP of Dango ecom: {otp}",
                from_='+16614656149',
                to=mobile
            )
        except Exception as e:
            return JsonResponse({'error': f'Failed to send OTP: {str(e)}'}, status=500)
        return JsonResponse({'message': 'OTP sent successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        try:
            mobile = request.POST.get('mobile')
            otp = request.POST.get('otp')
            full_name = request.POST.get('full_name', '')  # Get full_name from request, default empty string
            if not mobile or not otp:
                return JsonResponse({'error': 'Mobile and OTP are required'}, status=400)
            # Format mobile number to E.164 if not already
            if not mobile.startswith('+'):
                mobile = '+91' + mobile  # Assuming India country code
            stored_otp, expiry = otp_store.get(mobile, (None, None))
            if stored_otp is None:
                return JsonResponse({'error': 'OTP not found. Please request a new one.'}, status=400)
            if time.time() > expiry:
                del otp_store[mobile]
                return JsonResponse({'error': 'OTP expired. Please request a new one.'}, status=400)
            if otp.strip() != stored_otp.strip():
                return JsonResponse({'error': 'Invalid OTP'}, status=400)
            # OTP is valid, authenticate or create user
            user, created = User.objects.get_or_create(mobile=mobile)
            if created and full_name:
                user.full_name = full_name
                user.save()
            # Log the user in (session-based)
            login(request, user)
            del otp_store[mobile]
            full_name = getattr(user, 'full_name', '')
            return JsonResponse({'message': 'OTP verified, user logged in', 'user': {'mobile': user.mobile, 'full_name': full_name}})
        except Exception as e:
            return JsonResponse({'error': f'Error verifying OTP: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def current_date(request):
    from django.utils.timezone import now
    return JsonResponse({'date': now().strftime('%Y-%m-%d')})

# Cart APIs

@csrf_exempt
@require_http_methods(["GET"])
def get_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    for product_id_str, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id_str))
            cart_items.append({
                'id': product.id,
                'product': {
                    'id': product.id,
                    'product_name': product.product_name,
                    'price': float(product.price),
                },
                'quantity': quantity,
            })
        except Product.DoesNotExist:
            continue
    return JsonResponse(cart_items, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product')
        quantity = data.get('quantity', 1)
        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)
        product = Product.objects.get(id=product_id)
    except (json.JSONDecodeError, Product.DoesNotExist):
        return JsonResponse({'error': 'Invalid product'}, status=400)

    cart = request.session.get('cart', {})
    current_quantity = cart.get(str(product_id), 0)
    cart[str(product_id)] = current_quantity + quantity
    request.session['cart'] = cart
    request.session.modified = True

    return JsonResponse({'message': 'Product added to cart', 'cart': cart})

@csrf_exempt
@require_http_methods(["POST"])
def increase_quantity(request, cart_item_id):
    cart = request.session.get('cart', {})
    if str(cart_item_id) in cart:
        cart[str(cart_item_id)] += 1
        request.session['cart'] = cart
        request.session.modified = True
        return JsonResponse({'message': 'Quantity increased', 'cart': cart})
    return JsonResponse({'error': 'Item not in cart'}, status=404)

@csrf_exempt
@require_http_methods(["POST"])
def decrease_quantity(request, cart_item_id):
    cart = request.session.get('cart', {})
    if str(cart_item_id) in cart:
        if cart[str(cart_item_id)] > 1:
            cart[str(cart_item_id)] -= 1
            request.session['cart'] = cart
            request.session.modified = True
            return JsonResponse({'message': 'Quantity decreased', 'cart': cart})
        else:
            return JsonResponse({'error': 'Quantity cannot be less than 1'}, status=400)
    return JsonResponse({'error': 'Item not in cart'}, status=404)

@csrf_exempt
@require_http_methods(["DELETE"])
def remove_from_cart(request, cart_item_id):
    cart = request.session.get('cart', {})
    if str(cart_item_id) in cart:
        del cart[str(cart_item_id)]
        request.session['cart'] = cart
        request.session.modified = True
        return JsonResponse({'message': 'Item removed from cart', 'cart': cart})
    return JsonResponse({'error': 'Item not in cart'}, status=404)

# Order Management APIs

# Order Management APIs

@csrf_exempt
@require_http_methods(["POST"])
def place_order(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'User ID is required'}, status=400)
        user = User.objects.get(id=user_id)
    except (json.JSONDecodeError, User.DoesNotExist):
        return JsonResponse({'error': 'Invalid user'}, status=400)

    cart = request.session.get('cart', {})
    if not cart:
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    order = Order.objects.create(user=user, order_date=timezone.now(), status='Pending')

    for product_id_str, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id_str))
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
        except Product.DoesNotExist:
            continue

    # Clear cart after order placed
    request.session['cart'] = {}
    request.session.modified = True

    return JsonResponse({'message': 'Order placed successfully', 'order_id': order.id})

@csrf_exempt
@require_http_methods(["GET"])
def get_orders(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Invalid user'}, status=400)

    orders = Order.objects.filter(user=user).order_by('-order_date')
    orders_data = []
    for order in orders:
        items = OrderItem.objects.filter(order=order)
        total_price = sum(item.price * item.quantity for item in items)
        total_quantity = sum(item.quantity for item in items)
        orders_data.append({
            'id': order.id,
            'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': order.status,
            'total_price': total_price,
            'total_quantity': total_quantity,
        })
    return JsonResponse(orders_data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    if order.status != 'Pending':
        return JsonResponse({'error': 'Order cannot be cancelled'}, status=400)

    order.status = 'Cancelled'
    order.save()
    return JsonResponse({'message': 'Order cancelled successfully'})