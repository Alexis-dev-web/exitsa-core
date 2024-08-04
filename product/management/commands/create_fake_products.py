import random
import string

from django.core.management.base import BaseCommand
from product.models import Product
from faker import Faker

class Command(BaseCommand):
    help = 'Create 100 fake users'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        def generate_sku():
            # Generate a SKU in the format of 'SKU-XXXXXX'
            return f"SKU-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
    
        for _ in range(125):
            Product.objects.create(
                sku=generate_sku(),
                name=fake.word(),
                description=fake.text(),
                base_pricing=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
                base_cost=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                in_existence=fake.random_int(min=0, max=500),
                type='PHYSIC',
                state='IN_STOCK',
            )

        self.stdout.write(self.style.SUCCESS('Successfully created fake products'))
