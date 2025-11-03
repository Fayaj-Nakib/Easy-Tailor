from django.db import models

# Create your models here.
from users.models import CustomUser
from services.models import TailorService

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_orders')
    tailor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='tailor_orders')
    service = models.ForeignKey(TailorService, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, default='Unpaid')
    created_at = models.DateTimeField(auto_now_add=True)
    # measurement
    MEASURE_CHOICES = (('regular','Regular'),('custom','Custom'))
    SIZE_CHOICES = (('XS','XS'),('S','S'),('M','M'),('L','L'),('XL','XL'),('XXL','XXL'),('XXXL','XXXL'))
    measurement_type = models.CharField(max_length=10, choices=MEASURE_CHOICES, default='regular')
    regular_size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True)
    custom_measurements = models.TextField(blank=True)
    design_preference = models.TextField(blank=True)

class OrderItem(models.Model):
    DELIVERY_CHOICES = (
        ('regular', 'Regular (7-10 days)'),
        ('emergency', 'Emergency (2-3 days)'),
    )
    SERVICE_CHOICES = (
        ('new', 'Make New Cloth'),
        ('alter', 'Alter Cloth'),
        ('repair', 'Repair damaged cloth'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(TailorService, on_delete=models.PROTECT)
    gender = models.CharField(max_length=10)
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES, default='new')
    # per-item measurement
    MEASURE_CHOICES = (('regular','Regular'),('custom','Custom'))
    SIZE_CHOICES = (('XS','XS'),('S','S'),('M','M'),('L','L'),('XL','XL'),('XXL','XXL'),('XXXL','XXXL'))
    measurement_type = models.CharField(max_length=10, choices=MEASURE_CHOICES, default='regular')
    regular_size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True)
    custom_measurements = models.TextField(blank=True)
    item_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='regular')
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
