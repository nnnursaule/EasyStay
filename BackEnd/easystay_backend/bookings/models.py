from django.db import models
from users.models import User

ALL_AMENITIES = [
    "Parking", "WiFi", "Gym", "Swimming Pool", "Playground", "Elevator",
    "Security", "Garden", "Shops", "Laundry", "CCTV", "Bike Parking"
]


AMENITIES_TRANSLATION = {
    "Parking": "Парковка",
    "WiFi": "WiFi",
    "Gym": "Фитнес-зал",
    "Swimming Pool": "Бассейн",
    "Playground": "Детская площадка",
    "Elevator": "Лифт",
    "Security": "Охрана",
    "Garden": "Сад",
    "Shops": "Магазины",
    "Laundry": "Прачечная",
    "CCTV": "Видеонаблюдение",
    "Bike Parking": "Велопарковка",
    "Supermarket": "Супермаркет",
    "Concierge Service": "Консьерж-сервис",
    "Green Zones": "Зеленые зоны отдыха",
    "Restaurant": "Ресторан",
    "Underground Parking": "Подземный паркинг"
}

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


    #Rules
    min_age = models.IntegerField(null=True, blank=True, default=18)
    max_age = models.IntegerField(null=True, blank=True, default=100)
    musical_instruments = models.CharField(
        max_length=20,
        choices=[("allowed", "Allowed"), ("negotiable", "Negotiable"), ("not_allowed", "Not Allowed")],
        default="negotiable",
        null=True,
        blank=True
    )
    gender_preference = models.CharField(
        max_length=20,
        choices=[("no_preference", "No preference"), ("male", "Male only"), ("female", "Female only")],
        default="no_preference",
        null=True,
        blank=True
    )
    pets_allowed = models.BooleanField(null=True, blank=True, default=False)
    tenant_type = models.CharField(
        max_length=50,
        choices=[("students_only", "Students only"), ("working_professionals", "Working professionals"),
                 ("anyone", "Anyone")],
        default="anyone",
        null=True,
        blank=True
    )
    smoking_policy = models.CharField(
        max_length=50,
        choices=[("inside", "Inside allowed"), ("outside_only", "Outside only"), ("not_allowed", "Not allowed")],
        default="outside_only",
        null=True,
        blank=True
    )
    guest_policy = models.CharField(
        max_length=50,
        choices=[("allowed", "Allowed"), ("overnight_allowed", "Overnight allowed"), ("restricted", "Restricted")],
        default="allowed",
        null=True,
        blank=True
    )
    quiet_hours_start = models.TimeField(null=True, blank=True, default="23:00")
    quiet_hours_end = models.TimeField(null=True, blank=True, default="07:00")

    def available_apartments_count(self):
        return self.apartments.filter(status="available").count()

    def get_existing_amenities(self):
        """Получить список удобств, которые есть у ЖК"""
        return self.amenities.split(", ") if self.amenities else []

    def get_missing_amenities(self):
        """Получить список удобств, которых нет у ЖК"""
        return [amenity for amenity in ALL_AMENITIES if amenity not in self.get_existing_amenities()]
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




class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="written_reviews")  # Кто оставил отзыв
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="reviews")  # Отзыв о квартире
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author} for {self.apartment}"
