from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now
import random
from datetime import timedelta



class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_landlord = models.BooleanField(default=False)  # Арендодатель или студент
    phone_number = models.CharField(max_length=15, unique=False, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(null=True, auto_now_add=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    #Proverka landlord
    id_card_photo = models.ImageField(upload_to='id_cards/', null=True, blank=True)
    ownership_doc = models.FileField(upload_to='ownership_docs/', null=True, blank=True)
    is_verified_landlord = models.BooleanField(default=False)

    #Proverka student
    student_id_photo = models.ImageField(upload_to='student_ids/', null=True, blank=True)
    is_student_verified = models.BooleanField(default=False)

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)

    about = models.TextField(blank=True, null=True)  # Описание арендатора
    experience = models.IntegerField(default=0, null=True)
    
    def __str__(self):
        return self.email





def generate_verification_code():
    return str(random.randint(1000, 9999))

def generate_expiration_time():
    return now() + timedelta(minutes=10)

class EmailVerification(models.Model):
    code = models.CharField(max_length=4, unique=True, default=generate_verification_code)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=generate_expiration_time)

    def __str__(self):
        return f'EmailVerification for {self.user.email}'

    def send_verification_email(self):
        subject = f'Your verification code for {self.user.username}'
        message = f'Hello {self.user.username},\n\nYour verification code is: {self.code}\nThis code is valid for 10 minutes.'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False
        )

    def is_expired(self):
        return now() >= self.expiration