from django.core.management.base import BaseCommand
from user.models import User
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from order.models import Order


class Command(BaseCommand):
    help = 'Create base profiles'

    def handle(self, *args, **kwargs):
        user_content_type = ContentType.objects.get_for_model(User)

        Permission.objects.create(
            codename='iam_change_password',
            name='IAM change password',
            content_type=user_content_type
        )

        order_content_type = ContentType.objects.get_for_model(Order)

        Permission.objects.create(
            codename='cancel_order',
            name='Cancel order',
            content_type=order_content_type
        )

        permission_seller = [
            'add_product',
            'view_product',
            'change_product',
            'iam_change_password',
            'cancel_order',
            'add_user',
        ]

        permission_client = [
            'add_order',
            'view_order',
            'change_order',
            'view_product',
            'iam_change_password',
            'cancel_order',
            'view_user',
            'add_orderproduct',
            'view_orderproduct',
            'delete_orderproduct',
            'change_orderproduct',
            'change_user',
            'view_group'
        ]

        permisison_admin = [
            'delete_user',
            'view_logentry',
            'add_group',
            'change_group',
            'view_permission',
            'add_store',
            'change_store',
            'delete_store',
            'view_store',
            'change_storehasproduct',
            'add_storehasproduct',
            'delete_storehasproduct',
            'view_storehasproduct',
            'delete_product'
        ]

        admin = Group.objects.create(
            name='ADMIN'
        )

        seller = Group.objects.create(
            name='SELLER'
        )

        client = Group.objects.create(
            name='CLIENT'
        )

        permission_client_add = Permission.objects.filter(
            codename__in=permission_client
        ).all()

        client.permissions.set(permission_client_add)

        permission_seller_add = Permission.objects.filter(
            codename__in=permission_seller
        ).all()

        permission_seller_add = permission_seller_add.union(permission_client_add)
        seller.permissions.set(permission_seller_add)

        permission_admin_add = Permission.objects.filter(
            codename__in=permisison_admin
        ).all()

        permission_admin_add = permission_admin_add.union(permission_seller_add)
        admin.permissions.set(permission_admin_add)

        self.stdout.write(self.style.SUCCESS('Successfully migrate'))
