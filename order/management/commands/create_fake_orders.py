import random

from faker import Faker
from django.core.management.base import BaseCommand
from user.models import User, UserRepository
from product.models import Product, ProductRepository
from order.models import Order, OrderProduct
from django.utils import timezone



class Command(BaseCommand):
    help = 'Create fake orders with related users and products'

    def handle(self, *args, **kwargs):
        fake = Faker()
        clients = User.objects.all()
        products = ProductRepository().get_all()
        
        # Create fake orders
        for _ in range(250):  # Adjust the number of orders as needed
            order = Order.objects.create(
                code=f'EXSL00{_}',
                number=_,
                status=random.choice(['CREATE', 'CANCELLED', 'SENT', 'DELIVERED', 'REJECTED']),
                type='SALE',
                client=random.choice(clients),
                total_price=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
                created_at=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone()),
                updated_at=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
            )
            
            if order.status == 'DELVERED':
                order.delivered_date = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
                order.save()

            for _ in range(random.randint(1, 5)):  # Adjust the number of items per order
                OrderProduct.objects.create(
                    price=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                    order=order,
                    product=random.choice(products),
                    quantity=fake.random_int(min=1, max=10)
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully created fake orders'))