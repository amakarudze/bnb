# Generated by Django 5.0.9 on 2024-10-07 11:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rooms", "0002_room_room_capacity_alter_room_date_created_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="photo",
            field=models.ImageField(upload_to="images"),
        ),
    ]