import uuid

from django.contrib.auth.models import (  # noqa: E501
    AbstractBaseUser,
    PermissionsMixin,
)

from .user_manager import CustomUserManager

from django.db import models


class User(AbstractBaseUser, PermissionsMixin):

    GENDER = [
        ('F', 'female'),
        ('M', 'male'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    second_last_name = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, null=True)
    birthday =  models.DateField(null=True)
    gender = models.CharField(max_length=2, choices=GENDER, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name"]

    @property
    def is_staff(self):
        return self.is_superuser
