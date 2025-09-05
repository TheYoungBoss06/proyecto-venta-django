from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal # Import Decimal
from django.utils.text import slugify # Import slugify

# Create your models here.
class FurnitureCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True) # Add slug field

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class FurnitureProduct(models.Model):
    category = models.ForeignKey(FurnitureCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image =models.ImageField(upload_to='product_images/')
    stock = models.PositiveIntegerField(default=1)

   

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(FurnitureProduct, through='CartItem')

    

class CartItem(models.Model):
    product = models.ForeignKey(FurnitureProduct, on_delete=models.CASCADE)
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    promotion = models.ForeignKey('Promotion', on_delete=models.SET_NULL, null=True, blank=True) # Optional promotion for the item

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('PROCESSING', 'Procesando'),
        ('SHIPPED', 'Enviado'),
        ('DELIVERED', 'Entregado'),
        ('CANCELLED', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # product_name = models.CharField(max_length=255) # Removed, now handled by OrderItem
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255)
    shipping_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    shipping_phone = models.CharField(max_length=20, blank=True, null=True)
    coupon = models.ForeignKey('Promotion', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING') # Added status field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} de {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(FurnitureProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2) # Price at the time of purchase
    discount_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) # Discount applied to this item at purchase

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"
    
    
class Review(models.Model):
    product = models.ForeignKey(FurnitureProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Reseña de {self.user.username} el {self.date}"


class Promotion(models.Model):
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    minimum_cart_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    publication_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/',null = True,blank=True)

    def __str__(self):
        return self.title
