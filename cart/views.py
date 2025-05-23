from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import CartItem


def cart_sidebar(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    html = render_to_string('cart/cart.html', {'cart_items': cart_items, 'total': total}, request=request)
    return JsonResponse({'html': html})


def cart_delete_item(request):
    item_id = request.POST.get('id')
    if not item_id:
        return JsonResponse({'success': False, 'error': 'No item id provided'})

    try:
        item = CartItem.objects.get(id=item_id, user=request.user)
        item.delete()
        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(i.get_total_price() for i in cart_items)
        return JsonResponse({'success': True, 'total': total})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})


def cart_change_quantity(request):
    item_id = request.POST.get('id')
    op = request.POST.get('op')  
    if not item_id or op not in ('plus', 'minus'):
        return JsonResponse({'success': False, 'error': 'Invalid parameters'})

    try:
        item = CartItem.objects.get(id=item_id, user=request.user)
        if op == 'plus':
            item.quantity += 1
        elif op == 'minus' and item.quantity > 1:
            item.quantity -= 1
        item.save()

        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(i.get_total_price() for i in cart_items)

        return JsonResponse({'success': True, 'quantity': item.quantity, 'total': total})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})