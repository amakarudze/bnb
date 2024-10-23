import uuid


from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin,
)

from django_countries.fields import CountryField


class UserManager(BaseUserManager):
    """Manager class for the custom user model. Implements methods for creating users with different groups and user priviledges."""

    def _create_user(self, email, first_name, last_name, password=None, **role_fields):
        """Creates a user."""
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

    def create_user(self, email, first_name, last_name, password=None, **role_fields):
        """Creates an ordinary user with limited priviledges and permissions. Used to create guest accounts."""
        user = self._create_user(email, first_name, last_name, password, **role_fields)
        group = Group.objects.get(name="Guests")
        user.groups.add(group)
        user.save(using=self._db)
        return user

    def create_staff(self, email, first_name, last_name, password=None, **role_fields):
        """Creates a staff account for front desk staff. Has more priviledges and permissions than guest bue less than manager or superuser."""
        role_fields.setdefault("is_staff", True)
        user = self._create_user(email, first_name, last_name, password, **role_fields)
        group = Group.objects.get(name="Staff")
        user.groups.add(group)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, password=None, **role_fields
    ):
        """Creates a superaccount for manager and systems admin staff. Has all priviledges and permissions in the system."""
        role_fields.setdefault("is_staff", True)
        role_fields.setdefault("is_superuser", True)
        return self._create_user(email, first_name, last_name, password, **role_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Guest user model that uses email as username, instead of the default username provided for by Django."""

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
        return f"{self.first_name} {self.last_name} - {self.email}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    """Model for Guest's details for the profile."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dob = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(blank_label="(Select country)")
    phone_number = models.CharField(max_length=20)

    class Meta:
        managed = True
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.get_full_name()
