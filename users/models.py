from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('tailor', 'Tailor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    shop_name = models.CharField(max_length=100, blank=True)
    default_regular_size = models.CharField(max_length=10, blank=True)
    default_custom_measurements = models.TextField(blank=True)

class Measurement(models.Model):
    PRODUCT_CHOICES = (
        ('shirt', 'Shirt'),
        ('panjabi', 'Panjabi'),
        ('pant', 'Pant'),
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='measurements')
    product_type = models.CharField(max_length=20, choices=PRODUCT_CHOICES)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.username} - {self.product_type}"