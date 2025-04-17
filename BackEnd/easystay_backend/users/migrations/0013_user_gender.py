# Generated by Django 5.0.1 on 2025-03-25 02:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0012_user_age"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("male", "Male"), ("female", "Female")],
                max_length=6,
                null=True,
            ),
        ),
    ]
