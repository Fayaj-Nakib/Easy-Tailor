from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='payment_list'),     # /payments/
    path('add/', views.payment_create, name='payment_create'), # /payments/add/
]
