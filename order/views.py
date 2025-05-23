from django.shortcuts import get_object_or_404
from products.models import Product
from cart.models import CartItem
from django.http import JsonResponse


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