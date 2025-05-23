from django.db import models
from users.models import User
from products.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'товар у кошику'
        verbose_name_plural = 'товари у кошику'

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity
    