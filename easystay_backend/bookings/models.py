from django.db import models
from users.models import User



class ResidentialComplex(models.Model):  # ЖК
    name = models.CharField(max_length=255, unique=True)  # Название ЖК
    address = models.CharField(max_length=255)  # Адрес ЖК
    city = models.CharField(max_length=100)  # Город
    description = models.TextField(blank=True, null=True)  # Описание ЖК
    built_year = models.IntegerField(blank=True, null=True)  # Год постройки
    developer = models.CharField(max_length=255, blank=True, null=True)  # Застройщик
    image = models.ImageField(upload_to='apartments_images', null=True)
    total_floors = models.IntegerField(null=True, blank=True)  # Количество этажей
    parking = models.BooleanField(default=False)  # Есть ли парковка
    amenities = models.TextField(blank=True, null=True) # Удобства

    def available_apartments_count(self):
        return self.apartments.filter(status="available").count()
    def __str__(self):
        return f"{self.name} ({self.city})"


class Apartment(models.Model):
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="apartments")
    title = models.CharField(max_length=255)  # Название ЖК или квартиры
    complex = models.ForeignKey(ResidentialComplex, on_delete=models.CASCADE, related_name="apartments", null=True)  # ЖК
    rooms = models.IntegerField()  # Количество комнат
    area = models.FloatField()  # Площадь в м²
    floor = models.IntegerField(null=True, blank=True)  # Этаж
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='apartments_images')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    apartment_number = models.CharField(max_length=10, null=True, blank=True)
    STATUS_CHOICES = [
        ("available", "Available"),
        ("booked", "Booked"),
        ("unavailable", "Unavailable"),
    ]

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="available")  # Доступность
    description = models.TextField(blank=True, null=True)  # Описание
    bathrooms = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.title}"




