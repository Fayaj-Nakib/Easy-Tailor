from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),          # /orders/
    path('add/', views.order_create, name='order_create'), # /orders/add/
    path('<int:id>/', views.order_detail, name='order_detail'), # /orders/1/
]
