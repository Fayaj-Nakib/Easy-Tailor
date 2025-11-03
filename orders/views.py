from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from services.models import TailorService
from django.contrib.auth.decorators import login_required
from decimal import Decimal

@login_required
def order_list(request):
    # Tailor actions handled here for PRG
    if request.user.role == 'tailor' and request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = (
            'toggle_payment' if 'toggle_payment' in request.POST else
            'confirm' if 'confirm' in request.POST else
            'deny' if 'deny' in request.POST else
            'cancel' if 'cancel' in request.POST else None
        )
        if order_id and action:
            order = get_object_or_404(Order, id=order_id)
            # lock rules: payment can change only from Unpaid -> Paid once; status only from Pending
            if action == 'toggle_payment' and order.payment_status == 'Unpaid':
                order.payment_status = 'Paid'
            elif action == 'confirm' and order.status == 'Pending':
                # apply optional discount before confirming
                try:
                    discount_val = float(request.POST.get('discount') or 0)
                except ValueError:
                    discount_val = 0
                if discount_val > 0:
                    order.discount = Decimal(str(discount_val))
                    order.total_price = max(Decimal('0'), order.total_price - order.discount)
                order.status = 'Confirmed'
            elif action == 'deny' and order.status == 'Pending':
                order.status = 'Denied'
            elif action == 'cancel' and order.status != 'Cancelled' and order.payment_status != 'Paid':
                order.status = 'Cancelled'
            order.save()
        return redirect('order_list')
    if request.user.role == 'tailor':
        orders = Order.objects.select_related('customer', 'service').all()
        return render(request, 'order_list.html', {'orders': orders, 'is_tailor': True})
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'order_list.html', {'orders': orders, 'is_tailor': False})

@login_required
def order_create(request):
    # Customers place orders; tailors should not place orders
    if request.user.role == 'tailor':
        return redirect('order_list')
    # Ensure baseline general services exist for customers (male/female items)
    old_names = ['Make New Cloth', 'Alter Cloth', 'Repair damaged cloth']
    if not TailorService.objects.exists() or TailorService.objects.count() < 10 or TailorService.objects.filter(name__in=old_names).exists():
        seed = [
            # name, gender, category, price
            ('Shirt', 'male', 'Topwear', 500),
            ('Pant', 'male', 'Bottomwear', 650),
            ('Blazer', 'male', 'Outerwear', 1800),
            ('Waistcoat', 'male', 'Outerwear', 900),
            ('Kurta/Panjabi', 'male', 'Ethnic', 800),
            ('Suit', 'male', 'Formal', 2700),
            ('Sherwani', 'male', 'Ethnic', 2800),
            ('Dress', 'female', 'One-piece', 900),
            ('Saree Blouse', 'female', 'Blouse', 600),
            ('Lehenga', 'female', 'Ethnic', 2600),
            ('Skirt', 'female', 'Bottomwear', 700),
            ('Top', 'female', 'Topwear', 550),
            ('Salwar Kameez', 'female', 'Ethnic', 1300),
            ('Abaya', 'female', 'Outerwear', 1200),
            ('Coat', 'female', 'Outerwear', 1600),
        ]
        # Remove old generic placeholders if present
        TailorService.objects.filter(name__in=old_names).delete()
        for name, gender, category, price in seed:
            TailorService.objects.get_or_create(
                name=name, gender=gender,
                defaults={'description': name, 'category': category, 'price': price}
            )
    else:
        # Backfill categories for existing baseline items if still 'General'
        category_map = {
            'Shirt': 'Topwear', 'Pant': 'Bottomwear', 'Blazer': 'Outerwear', 'Waistcoat': 'Outerwear',
            'Kurta/Panjabi': 'Ethnic', 'Suit': 'Formal', 'Sherwani': 'Ethnic',
            'Dress': 'One-piece', 'Saree Blouse': 'Blouse', 'Lehenga': 'Ethnic', 'Skirt': 'Bottomwear',
            'Top': 'Topwear', 'Salwar Kameez': 'Ethnic', 'Abaya': 'Outerwear', 'Coat': 'Outerwear'
        }
        for svc in TailorService.objects.all():
            if svc.category == 'General' and svc.name in category_map:
                svc.category = category_map[svc.name]
                svc.save(update_fields=['category'])
    services = TailorService.objects.all()
    tailors = None
    try:
        from users.models import CustomUser
        tailors = CustomUser.objects.filter(role='tailor')
    except Exception:
        tailors = []
    if request.method == 'POST':
        tailor_id = request.POST.get('tailor')
        genders = request.POST.getlist('gender[]')
        service_ids = request.POST.getlist('service[]')
        service_types = request.POST.getlist('service_type[]')
        quantities = request.POST.getlist('quantity[]')
        deliveries = request.POST.getlist('delivery[]')
        meas_types = request.POST.getlist('measurement_type[]')
        sizes = request.POST.getlist('regular_size[]')
        customs = request.POST.getlist('custom_measurements[]')
        chosen_tailor = None
        if tailor_id:
            try:
                from users.models import CustomUser
                chosen_tailor = CustomUser.objects.get(id=tailor_id)
            except CustomUser.DoesNotExist:
                chosen_tailor = None
        order = Order.objects.create(customer=request.user, tailor=chosen_tailor, service=services.first(), quantity=1, total_price=0)
        # measurements
        m_type = request.POST.get('measurement_type') or 'regular'
        order.measurement_type = m_type
        if m_type == 'regular':
            order.regular_size = request.POST.get('regular_size') or ''
        else:
            fields = ['length','chest','hand','shoulder','calf','arm','waist']
            values = {f: request.POST.get(f) for f in fields}
            order.custom_measurements = '\n'.join([f"{k}: {v}" for k, v in values.items() if v])
        order.design_preference = request.POST.get('design_preference') or ''
        order.save()
        total_price = 0
        for idx, (g, sid, s_type, qty, d) in enumerate(zip(genders, service_ids, service_types, quantities, deliveries)):
            if not sid:
                continue
            service = get_object_or_404(TailorService, id=sid)
            qty_int = max(1, int(qty or 1))
            base = float(service.price)
            # price adjustments by service type
            service_mult = 1.0 if s_type == 'new' else (0.4 if s_type == 'alter' else 0.25)
            multiplier = 1.3 if d == 'emergency' else 1.0
            unit_price = base * service_mult
            line_total = unit_price * qty_int * multiplier
            m_type = (meas_types[idx] if idx < len(meas_types) else 'regular') or 'regular'
            size_val = sizes[idx] if idx < len(sizes) else ''
            custom_val = customs[idx] if idx < len(customs) else ''
            OrderItem.objects.create(
                order=order,
                service=service,
                gender=g,
                service_type=s_type,
                quantity=qty_int,
                unit_price=unit_price,
                delivery_type=d,
                line_total=line_total,
                measurement_type=m_type,
                regular_size=size_val if m_type == 'regular' else '',
                custom_measurements=custom_val if m_type == 'custom' else '',
            )
            total_price += line_total
        order.total_price = total_price
        order.save(update_fields=['total_price'])
        return redirect('order_list')
    return render(request, 'order_create.html', {'services': services, 'tailors': tailors})

@login_required
def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    # Allow tailor to update discount, payment status, and confirm/deny
    if request.user.role == 'tailor' and request.method == 'POST':
        if 'cancel' in request.POST:
            order.status = 'Cancelled'
            order.save(update_fields=['status'])
            return redirect('order_detail', id=order.id)
        if 'confirm' in request.POST:
            order.status = 'Confirmed'
            order.save(update_fields=['status'])
            return redirect('order_detail', id=order.id)
        if 'deny' in request.POST:
            order.status = 'Denied'
            order.save(update_fields=['status'])
            return redirect('order_detail', id=order.id)
        discount = request.POST.get('discount')
        payment_status = request.POST.get('payment_status')
        if discount is not None:
            try:
                order.discount = Decimal(discount)
            except ValueError:
                pass
        if payment_status:
            order.payment_status = payment_status
        # Recalculate total after discount
        order.total_price = order.service.price * order.quantity - order.discount
        order.save()
        return redirect('order_detail', id=order.id)
    if request.user.role == 'customer' and request.method == 'POST':
        if 'cancel' in request.POST and order.status == 'Pending' and order.customer_id == request.user.id:
            order.status = 'Cancelled'
            order.save(update_fields=['status'])
            return redirect('order_list')
    return render(request, 'order_detail.html', {'order': order, 'is_tailor': request.user.role == 'tailor'})
