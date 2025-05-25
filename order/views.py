from django.shortcuts import get_object_or_404,render,HttpResponseRedirect
from products.models import Product
from cart.models import CartItem
from django.http import JsonResponse
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.models import CartItem
from django.urls import reverse
from django.contrib import messages

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
        if not cart_items.exists():
            messages.warning(request, 'Ваш кошик порожній. Додайте товари перед оформленням замовлення.')
            return HttpResponseRedirect(reverse('checkout')) 
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                delivery_name=form.cleaned_data['delivery_name'],
                phone=form.cleaned_data['phone'],
                delivery_address=form.cleaned_data['delivery_address'],
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    total_price=item.product.price * item.quantity,
                )

            CartItem.objects.filter(user=request.user).delete()

            messages.success(request, 'Замовлення успішно оформлено! Дякуємо що обираєте нас!')
            return HttpResponseRedirect(reverse('home'))

    else:
        form = CheckoutForm(user=request.user)
    return render(request, 'order\сheckout.html', {'form': form, 'cart_items': cart_items, 'total': total})



def order_history(request):
    orders = request.user.orders.prefetch_related('items__product').order_by('-created_at')
    for order in orders:
        order.total_sum = sum(item.get_total_price() for item in order.items.all())
    
    return render(request, 'order/order_history.html', {'orders': orders})





