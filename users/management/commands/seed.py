from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from services.models import TailorService
from orders.models import Order, OrderItem

User = get_user_model()

class Command(BaseCommand):
    help = "Seed database with demo users, services, and a sample order"

    def handle(self, *args, **options):
        # Create users
        tailor, _ = User.objects.get_or_create(
            username='tailor1', defaults={
                'role': 'tailor',
                'email': 'tailor1@example.com',
                'first_name': 'Taylor',
                'last_name': 'Smith',
                'phone': '0123456789',
                'shop_name': 'Tailor One'
            }
        )
        if not tailor.has_usable_password():
            tailor.set_password('tailor123')
            tailor.save()

        customer, _ = User.objects.get_or_create(
            username='customer1', defaults={
                'role': 'customer',
                'email': 'customer1@example.com',
                'first_name': 'Alex',
                'last_name': 'Doe',
                'phone': '0198765432',
                'address': '123 Demo Street'
            }
        )
        if not customer.has_usable_password():
            customer.set_password('customer123')
            customer.save()

        # Services (idempotent via get_or_create)
        seed_services = [
            ('Shirt', 'male', 'Topwear', 500),
            ('Pant', 'male', 'Bottomwear', 650),
            ('Kurta/Panjabi', 'male', 'Ethnic', 800),
            ('Dress', 'female', 'One-piece', 900),
            ('Saree Blouse', 'female', 'Blouse', 600),
            ('Salwar Kameez', 'female', 'Ethnic', 1300),
        ]
        created = 0
        for name, gender, category, price in seed_services:
            _, was_created = TailorService.objects.get_or_create(
                name=name, gender=gender,
                defaults={'description': name, 'category': category, 'price': price}
            )
            created += int(was_created)

        # Sample order only if none exists yet
        if not Order.objects.exists():
            services = list(TailorService.objects.all()[:2])
            order = Order.objects.create(
                customer=customer,
                tailor=tailor,
                service=services[0],
                quantity=1,
                total_price=0,
                status='Pending',
                payment_status='Unpaid',
                measurement_type='regular',
                regular_size='M',
                design_preference='Clean finish, minimal seams.'
            )
            total = 0
            # Add two items
            for svc in services:
                unit = float(svc.price)
                qty = 1
                line = unit * qty
                OrderItem.objects.create(
                    order=order,
                    service=svc,
                    gender=svc.gender,
                    service_type='new',
                    quantity=qty,
                    unit_price=unit,
                    delivery_type='regular',
                    line_total=line,
                    measurement_type='regular',
                    regular_size='M'
                )
                total += line
            order.total_price = total
            order.save(update_fields=['total_price'])

        self.stdout.write(self.style.SUCCESS('Seed completed. Users: tailor1/customer1 (passwords: tailor123 / customer123).'))

