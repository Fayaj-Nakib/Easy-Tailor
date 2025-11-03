from django.db import models

# Create your models here.
class TailorService(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('unisex', 'Unisex'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    category = models.CharField(max_length=50, default='General')

    def __str__(self):
        return self.name