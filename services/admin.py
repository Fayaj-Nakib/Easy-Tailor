from django.contrib import admin

# Register your models here.
from .models import TailorService

@admin.register(TailorService)
class TailorServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']
