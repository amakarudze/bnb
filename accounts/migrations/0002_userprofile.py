# Generated by Django 5.0.9 on 2024-10-01 22:17

import django.db.models.deletion
import django_countries.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("dob", models.DateField()),
                ("address", models.CharField(max_length=200)),
                ("city", models.CharField(max_length=100)),
                ("postal_code", models.CharField(max_length=10)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("phone_number", models.CharField(max_length=20)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "User Profile",
                "verbose_name_plural": "User Profiles",
                "managed": True,
            },
        ),
    ]