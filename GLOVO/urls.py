"""
URL configuration for GLOVO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
from django.urls import path,include
from main.views import home
from products.views import restaurant_menu,product_detail,menu,product_modal
from users.views import login,registration,logout
from cart.views import cart_sidebar,cart_delete_item,cart_change_quantity
from order.views import add_to_cart_ajax


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('menu/<slug:slug>/', restaurant_menu, name='restaurant_menu'),
    path('menu/<slug:restaurant_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
    path('menu/', menu, name='menu'),
    path('login/', login,name='login'),
    path('registration/', registration, name='registration'),
    path('logout/',logout, name='logout'),
    path('cart/sidebar/', cart_sidebar, name='cart_sidebar'),
    path('cart/delete-item/', cart_delete_item, name='cart_delete_item'),
    path('cart/change-quantity/', cart_change_quantity, name='cart_change_quantity'),
    path('products/<int:pk>/modal/', product_modal, name='product_modal'),
    path('cart/add_ajax/', add_to_cart_ajax, name='add_to_cart_ajax'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



