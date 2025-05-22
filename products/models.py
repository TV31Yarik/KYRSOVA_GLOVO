from django.db import models
from django.urls import reverse

class Restaurant(models.Model):
    name=models.CharField(max_length=25,unique=True)
    slug=models.SlugField(max_length=25,unique=True)
    description=models.TextField()
    image_logo=models.ImageField(upload_to='restaurant_logos/')

    class Meta:
        ordering=['name']
        indexes=[
            models.Index(fields=['name','slug']),
            ]
        verbose_name='заклад'
        verbose_name_plural= 'заклади'

    def __str__(self):
        return self.name    

class Category(models.Model):
    name=models.CharField(max_length=25,unique=True)
    restaurant=models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)

    class Meta:
        ordering=['name']
        indexes=[
            models.Index(fields=['name']),
            ]
        verbose_name='категорія'
        verbose_name_plural= 'категорії'
    
    def __str__(self):
        return self.name  
    
    
class Product(models.Model):
    name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    short_description=models.TextField()
    description=models.TextField()
    energy_value=models.TextField()
    price=models.DecimalField(max_digits=10,
                               decimal_places=2)
    main_image=models.ImageField(upload_to='main_product/')
    available=models.BooleanField(default=True)
    discount=models.DecimalField(default=0.00,max_digits=4,decimal_places=2)
    restaurant=models.ForeignKey(to=Restaurant, on_delete=models.CASCADE)
    category=models.ForeignKey(to=Category,on_delete=models.CASCADE)

    class Meta:
        ordering=['name']
        indexes=[
            models.Index(fields=['name','slug']),
            ]
        verbose_name='товар'
        verbose_name_plural= 'товари'
    
    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse("main:product_detail",
                       args=[self.slug])
    
    def sel_price(self):
        if self.discount>0:
            return round(self.price-self.price*self.discount/100,2)
        return self.price

class ProductImage(models.Model):
    product=models.ForeignKey(to=Product, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='product/')

    class Meta:
        ordering=['product']
        verbose_name='фото'
        verbose_name_plural= 'фото'
    
    def __str__(self):
        return self.image.name
