import uuid, random
from datetime import timedelta
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from django import forms
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm, UserCreationForm
from .models import User, EmailVerification

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
    ROLE_CHOICES = [
        (False, 'Студент'),
        (True, 'Арендодатель')
    ]

    role_choice = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(),
        label="Выберите роль"
    )

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input the first name:'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Input the last name:'
    }))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number'
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
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

        if not email and not phone_number:
            raise forms.ValidationError("Either email or phone number must be provided.")

        return cleaned_data

    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number", "email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_landlord = self.cleaned_data['role_choice'] == 'True'  # Определяем роль пользователя

        if commit:
            user.save()
            expiration = now() + timedelta(hours=48)
            code = str(random.randint(1000, 9999))
            record = EmailVerification.objects.create(code=code, user=user, expiration=expiration)
            record.send_verification_email()

        return user


class ProfileForm(UserChangeForm):
    delete_image = forms.BooleanField(
        required=False, label="Удалить изображение"
    )
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control py-4'}),
        required=False,
        label="Старый пароль"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control py-4'}),
        required=False,
        label="Новый пароль"
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "image", "delete_image", "username", "email")

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")

        # Проверяем, если введён новый пароль, но не введён старый
        if new_password and not old_password:
            self.add_error("old_password", "Введите старый пароль перед сменой нового.")

        # Проверка корректности старого пароля
        if old_password and not check_password(old_password, self.instance.password):
            self.add_error("old_password", "Старый пароль неверный.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Удаление изображения, если выбрано
        if self.cleaned_data.get("delete_image"):
            user.image.delete(save=False)
            user.image = None

        # Изменение пароля, если он введён
        if self.cleaned_data.get("new_password"):
            user.set_password(self.cleaned_data["new_password"])

        if commit:
            user.save()
        return user


class VerificationCodeForm(forms.Form):
    digit1 = forms.CharField(max_length=1, required=True)
    digit2 = forms.CharField(max_length=1, required=True)
    digit3 = forms.CharField(max_length=1, required=True)
    digit4 = forms.CharField(max_length=1, required=True)