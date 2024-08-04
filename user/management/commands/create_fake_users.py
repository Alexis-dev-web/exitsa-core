from io import StringIO
from django.core.management.base import BaseCommand
from user.models import User, GroupRepository
from faker import Faker

class Command(BaseCommand):
    help = 'Create 100 fake users'

    def handle(self, *args, **kwargs):
        group_repository = GroupRepository()
        group = group_repository.get_by_name('CLIENT')
        group_seller = group_repository.get_by_name('SELLER')
        admin = group_repository.get_by_name('ADMIN')
        
        fake = Faker()
        
        for _ in range(50):
            user = User.objects._create_user(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password=fake.password()
            )
            
            user.groups.set([group])

        for _ in range(30):
            user = User.objects._create_user(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password=fake.password()
            )
            
            user.groups.set([group_seller])

        for _ in range(25):
            user = User.objects._create_user(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password=fake.password()
            )
            
            user.groups.set([admin])

        self.stdout.write(self.style.SUCCESS('Successfully created fake users'))
