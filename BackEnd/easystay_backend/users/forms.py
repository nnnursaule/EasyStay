import uuid
from datetime import timedelta

from django.utils.timezone import now
from . models import User, EmailVerification
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input the username:'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input the password'
    }))
    class Meta:
        model = User
        fields = ("username", "password")


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input the first_name:'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input the last_name:'
    }))

    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number'},

    ))


    email = forms.CharField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input the email:'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input the username:'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input the password'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Confirm the password'
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")

        # Преобразуем пустые строки в None
        if email == "":
            email = None
        if phone_number == "":
            phone_number = None

        if not email and not phone_number:
            raise forms.ValidationError("Either email or phone number must be provided.")

        # Обновляем данные формы
        cleaned_data["email"] = email
        cleaned_data["phone_number"] = phone_number
        print(cleaned_data)  # Добавь перед return

        return cleaned_data

    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number", "email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        return user



class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "image", "username", "email")

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'readonly': 'True'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'readonly': 'True'
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input'
    }), required=False)