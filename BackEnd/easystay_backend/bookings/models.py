from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import timedelta
from django.utils import timezone

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
    ALMATY_REGIONS = [
        ("almaly", "Алмалинский"),
        ("auyezov", "Ауэзовский"),
        ("bostandyk", "Бостандыкский"),
        ("medeu", "Медеуский"),
        ("nauryzbay", "Наурызбайский"),
        ("turksib", "Турксибский"),
        ("zhetysu", "Жетысуский"),
        ("alatau", "Алатауский"),
    ]
    name = models.CharField(max_length=255, unique=True)  # Название ЖК
    address = models.CharField(max_length=255)  # Адрес ЖК
    region = models.CharField(max_length=50, choices=ALMATY_REGIONS, default="almaly", null=True)
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
        return f"{self.name} ({self.address})"


class Apartment(models.Model):
    landlord = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="apartments")
    is_top = models.BooleanField(default=False)
    title = models.CharField(max_length=255)  # Название ЖК или квартиры
    address = models.CharField(max_length=255, null=True)
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

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

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

    amenities = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        default=list,
        help_text="Удобства квартиры (например: WiFi, Parking)"
    )

    def __str__(self):
        return f"{self.title}"

# class Apartment(models.Model):
#     landlord = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="apartments")
#     title = models.CharField(max_length=255)  # Название ЖК или квартиры
#     address = models.CharField(max_length=255, null=True)
#     complex = models.ForeignKey(ResidentialComplex, on_delete=models.CASCADE, related_name="apartments", null=True)  # ЖК
#     rooms = models.IntegerField()  # Количество комнат
#     area = models.FloatField()  # Площадь в м²
#     floor = models.IntegerField(null=True, blank=True)  # Этаж
#     price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     image = models.ImageField(upload_to='apartments_images')
#     price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
#     apartment_number = models.CharField(max_length=10, null=True, blank=True)
#     STATUS_CHOICES = [
#         ("available", "Available"),
#         ("booked", "Booked"),
#         ("unavailable", "Unavailable"),
#     ]
#
#     status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="available")  # Доступность
#     description = models.TextField(blank=True, null=True)  # Описание
#     bathrooms = models.IntegerField(default=1)
#
#     def __str__(self):
#         return f"{self.title}"




class Review(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="written_reviews")  # Кто оставил отзыв
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="reviews")  # Отзыв о квартире
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='users_images/', blank=True, null=True)

    def __str__(self):
        return f"Review by {self.author} for {self.apartment}"


class Favourite(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="user_favourites")
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="apartment_favourited")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'apartment')

    def __str__(self):
        return f"{self.user} -> {self.apartment}"


class Complaint(models.Model):
    REASONS = [
        ('incorrect_info', 'The ad contains incorrect information'),
        ('fake_home', 'This is not a real home'),
        ('scam', 'This is a scam'),
        ('offensive', 'This is offensive'),
        ('other', 'The problem is different'),
    ]

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    apartment = models.ForeignKey('bookings.Apartment', on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=REASONS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'apartment')  # 👈 ограничение на уникальность жалобы

    def __str__(self):
        return f"{self.user} - {self.get_reason_display()}"



class Feedback(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='users_images/', blank=True, null=True)

    def __str__(self):
        return f"Feedback from {self.name} ({self.rating} stars)"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('student', 'Student'),
        ('landlord', 'Landlord'),
    ]

    TYPE_CHOICES = [
        ('single', 'Один'),
        ('shared', 'С подселением'),
    ]

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    type_of_booking = models.CharField(max_length=10, choices=TYPE_CHOICES)
    comment = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.name} for {self.apartment}"

class TopPromotion(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE, related_name='top_promotion')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def is_active(self):
        return self.end_date >= timezone.now()

    def __str__(self):
        return f"TOP: {self.apartment.title} до {self.end_date}"