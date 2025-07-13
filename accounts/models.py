from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('customer','Customer'),
    )
    role = models.CharField(max_length=30,choices=ROLE_CHOICES,default='customer')

    def __str__(self):
        return f'{self.username} {{self.role}}'
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"