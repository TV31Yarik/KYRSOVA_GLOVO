from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Category, Product
from django.db.models import Q

def restaurant_menu(request, slug ):
    restaurant = get_object_or_404(Restaurant, slug=slug)
    categories = Category.objects.filter(restaurant=restaurant)


    category_id = request.GET.get('category')
    sort_option=request.GET.get('sort')
    search_query = request.GET.get('q')
    
    if category_id:
        active_category = get_object_or_404(Category, id=category_id, restaurant=restaurant)
        products = Product.objects.filter(restaurant=restaurant, category=active_category, available=True)
    else:
        active_category = None
        products = Product.objects.filter(restaurant=restaurant, available=True)
    if search_query:
        products=products.filter(Q(name__icontains=search_query))
        
    if sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')
    elif sort_option == 'alpha':
        products = products.order_by('name')    
    
    return render(request, 'products/products_list/products_list.html', {
        'restaurant': restaurant,
        'categories': categories,
        'products': products,
        'active_category': active_category,
    })

def product_detail(request, restaurant_slug, product_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    product = get_object_or_404(Product, restaurant=restaurant, slug=product_slug)
    return render(request, 'products/products_detail/products_detail.html', {
        'product': product
    })

def menu(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'products/menu/menu.html', {'restaurants': restaurants})

def product_modal(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'order/order.html', {'product': product})