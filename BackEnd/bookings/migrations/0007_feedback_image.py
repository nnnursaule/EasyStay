# Generated by Django 5.0.1 on 2025-04-30 00:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookings", "0006_feedback"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="feedback_images/"
            ),
        ),
    ]
