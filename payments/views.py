from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .models import Payment
from orders.models import Order
from django.contrib.auth.decorators import login_required

@login_required
def payment_list(request):
    payments = Payment.objects.filter(order__customer=request.user)
    return render(request, 'payment_list.html', {'payments': payments})

@login_required
def payment_create(request):
    orders = Order.objects.filter(customer=request.user, payment__isnull=True)
    if request.method == 'POST':
        order_id = request.POST.get('order')
        method = request.POST.get('method')
        order = Order.objects.get(id=order_id)
        Payment.objects.create(order=order, amount=order.total_price, method=method)
        return redirect('payment_list')
    return render(request, 'payment_create.html', {'orders': orders})
