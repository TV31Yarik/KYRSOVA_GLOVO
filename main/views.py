from django.shortcuts import render
from products.models import Restaurant


def home(request):
    restaurants = Restaurant.objects.all()[:3]
    return render(request, 'main/index/index.html', {'restaurants': restaurants ,})

