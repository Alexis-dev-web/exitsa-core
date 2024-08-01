from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, first_name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, first_name=None, email=None, password=None, **extra_fields):  # noqa: E501
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(first_name, email, password, **extra_fields)

    def create_superuser(self, first_name=None, email=None, password=None, **extra_fields):  # noqa: E501
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(first_name, email, password, **extra_fields)

