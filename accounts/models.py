import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager class for the custom user model. Implements methods for creating users with different groups and user priviledges."""

    def create_user(self, email, first_name, last_name, password=None, **role_fields):
        """Creates an ordinary user with limited priviledges and permissions. Used to create guest accounts."""
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            **role_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, first_name, last_name, password=None, **role_fields):
        """Creates a staff account for front desk staff. Has more priviledges and permissions than guest bue less than manager or superuser."""
        role_fields.setdefault("is_staff", True)
        return self.create_user(email, first_name, last_name, password, **role_fields)

    def create_superuser(
        self, email, first_name, last_name, password=None, **role_fields
    ):
        """Creates a superaccount for manager and systems admin staff. Has all priviledges and permissions in the system."""
        role_fields.setdefault("is_staff", True)
        role_fields.setdefault("is_superuser", True)
        return self.create_user(email, first_name, last_name, password, **role_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Customer user model that uses email as username, instead of the default username provided for by Django."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    class Meta:
        managed = True

    def __str__(self):
        """String representation of the model."""
        return f"{self.first_name} {self.last_name}"
