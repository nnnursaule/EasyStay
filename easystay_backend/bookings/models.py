from django.db import models




# class Apartment(models.Model):
#     landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="apartments")
#     title = models.CharField(max_length=255)  # Название ЖК или квартиры
#     description = models.TextField()  # Описание
#     address = models.CharField(max_length=255)  # Адрес
#     city = models.CharField(max_length=100)
#     rooms = models.IntegerField()  # Количество комнат
#     area = models.FloatField()  # Площадь в м²
#     floor = models.IntegerField(null=True, blank=True)  # Этаж
#     price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.title} ({self.address})"
