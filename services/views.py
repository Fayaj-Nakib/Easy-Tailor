from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TailorService

@login_required
def service_list(request):
    # Only tailors can manage service catalog
    if request.user.role != 'tailor':
        return redirect('order_list')
    services = TailorService.objects.all()
    return render(request, 'service_list.html', {'services': services})

@login_required
def service_add(request):
    if request.user.role != 'tailor':
        return redirect('order_list')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        gender = request.POST.get('gender') or 'unisex'
        category = request.POST.get('category') or 'General'
        TailorService.objects.create(name=name, description=description, price=price, gender=gender, category=category)
        return redirect('service_list')
    return render(request, 'service_add.html')

@login_required
def service_detail(request, id):
    if request.user.role != 'tailor':
        return redirect('order_list')
    service = get_object_or_404(TailorService, id=id)
    return render(request, 'service_detail.html', {'service': service})
