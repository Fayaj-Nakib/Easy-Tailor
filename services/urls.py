from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),       # /services/
    path('add/', views.service_add, name='service_add'),    # /services/add/
    path('<int:id>/', views.service_detail, name='service_detail'), # /services/1/
]
