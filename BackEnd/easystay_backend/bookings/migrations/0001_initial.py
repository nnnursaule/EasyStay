# Generated by Django 5.1.6 on 2025-03-11 07:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Apartment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("rooms", models.IntegerField()),
                ("area", models.FloatField()),
                ("floor", models.IntegerField(blank=True, null=True)),
                (
                    "price_per_month",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("image", models.ImageField(upload_to="apartments_images")),
                (
                    "landlord",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="apartments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
