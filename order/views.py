from django.shortcuts import get_object_or_404,render,HttpResponseRedirect,HttpResponse
from products.models import Product
from cart.models import CartItem
from django.http import JsonResponse
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.models import CartItem
from django.urls import reverse
from django.contrib import messages
import stripe
from django.conf import settings
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_SECRET_KEY


def add_to_cart_ajax(request):
    print('Отримано запит:', request.POST)
    print('Користувач:', request.user)
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({'success': True, 'message': 'Товар додано до кошика'})




def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            request.session['delivery_name'] = form.cleaned_data['delivery_name']
            request.session['phone'] = form.cleaned_data['phone']
            request.session['delivery_address'] = form.cleaned_data['delivery_address']
        
            return HttpResponseRedirect(reverse('create_checkout_session'))
    else:
        form = CheckoutForm(user=request.user)

    return render(request, 'order/сheckout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total
    })



def order_history(request):
    orders = request.user.orders.prefetch_related('items__product').order_by('-created_at')
    for order in orders:
        order.total_sum = sum(item.get_total_price() for item in order.items.all())
    
    return render(request, 'order/order_history.html', {'orders': orders})


def create_checkout_session(request):
    cart_items = CartItem.objects.filter(user=request.user)
    line_items = []
    for item in cart_items:
        print(request.build_absolute_uri(item.product.main_image.url))
        line_items.append({
            'price_data': {
                'currency': 'uah',
                'unit_amount': int(item.product.price * 100),  
                'product_data': {
                    'name': item.product.name,
                    'images': [request.build_absolute_uri(item.product.main_image.url)],
                },
            },
            'quantity': item.quantity,
        })
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url = request.build_absolute_uri(reverse('payment_success')),
            cancel_url = request.build_absolute_uri(reverse('checkout')),
        )
    except Exception as e:
        return HttpResponse(str(e))

    return redirect(checkout_session.url, code=303)

def payment_success(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        messages.warning(request, 'Кошик порожній або замовлення вже оброблено.')
        return HttpResponseRedirect(reverse('home'))
    delivery_name = request.session.get('delivery_name', '-')
    phone = request.session.get('phone', '-')
    delivery_address = request.session.get('delivery_address', '-')

    order = Order.objects.create(
        user=user,
        delivery_name=delivery_name,
        phone=phone,
        delivery_address=delivery_address,
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            total_price=item.product.price * item.quantity,
        )

    cart_items.delete()
    messages.success(request, 'Замовлення успішно оформлено! Дякуємо що обираєте нас!')
    return HttpResponseRedirect(reverse('home'))




