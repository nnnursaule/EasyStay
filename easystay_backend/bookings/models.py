from django.db import models
from users.models import User


class Apartment(models.Model):
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="apartments")
    title = models.CharField(max_length=255)  # Название ЖК или квартиры
    description = models.TextField()  # Описание
    address = models.CharField(max_length=255)  # Адрес
    city = models.CharField(max_length=100)
    rooms = models.IntegerField()  # Количество комнат
    area = models.FloatField()  # Площадь в м²
    floor = models.IntegerField(null=True, blank=True)  # Этаж
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='apartments_images')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_day = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} ({self.address})"


