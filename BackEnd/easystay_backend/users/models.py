from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_landlord = models.BooleanField(default=False)  # Арендодатель или студент
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)


    def __str__(self):
        return self.email



class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for [self.user.email]'

    def send_verification_email(self):
        link = reverse("users:verify", kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Confirming the email for {self.user.username}'
        message = 'For confirming the account for {} please go to following link: {}'.format(
            self.user.username,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False
        )

    def is_expired(self):
        return True if now() >= self.expiration else False