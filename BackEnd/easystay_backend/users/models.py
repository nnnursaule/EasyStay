from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_landlord = models.BooleanField(default=False)  # Арендодатель или студент
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)



    def __str__(self):
        return self.email


