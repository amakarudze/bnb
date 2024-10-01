# Generated by Django 5.0.9 on 2024-10-01 22:17

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("photo", models.ImageField(upload_to="")),
                ("host", models.CharField(max_length=100)),
                ("venue", models.CharField(max_length=255)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("min_participants", models.IntegerField(default=0)),
                ("max_participants", models.IntegerField(default=0)),
                ("num_participants", models.IntegerField(default=0)),
                ("fully_booked", models.BooleanField(default=False)),
                ("price", models.FloatField(default=0)),
                (
                    "age_restrictions",
                    models.CharField(
                        choices=[
                            ("No age restrictions", "No age restrictions"),
                            ("Below 12 years", "Below 12 years"),
                            ("12 years+", "12 years+"),
                            ("18 years+", "18 years+"),
                            ("21 years+", "21 years+"),
                            ("50 yeards+", "50 years+"),
                            ("60 years+", "60 years+"),
                        ],
                        max_length=30,
                    ),
                ),
                ("additional_information", models.TextField(blank=True, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                "managed": True,
            },
        ),
    ]