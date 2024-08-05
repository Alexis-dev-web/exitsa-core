import random
import string

from django.core.management.base import BaseCommand
from store.models import Store
from faker import Faker

class Command(BaseCommand):
    help = 'Create 10 fake stores'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(10):
            Store.objects.create(
                name=fake.word(),
                description=fake.text(),
                type='BOTH',
            )

        self.stdout.write(self.style.SUCCESS('Successfully created fake stores'))
