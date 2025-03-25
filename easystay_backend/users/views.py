from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model, login
from . forms import UserRegistrationForm, UserLoginForm, ProfileForm, VerificationCodeForm
from .models import  User, EmailVerification
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from datetime import timedelta
from bookings.models import Review, Apartment
import random


from django.views import View
class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context

User = get_user_model()


class UserCreationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = "users/signup.html"
    form_class = UserRegistrationForm
    success_message = "Поздравляем, вы успешно зарегистрированы!"
    title = "Store - Регистрация"

    def form_valid(self, form):
        user = form.save()

        expiration = now() + timedelta(hours=48)
        verification_record = EmailVerification.objects.create(
            code=str(random.randint(1000, 9999)),  # Случайный 4-значный код
            user=user,
            expiration=expiration
        )

        verification_record.send_verification_email()

        login(self.request, user)

        return redirect(reverse("users:verify-email"))

    def form_invalid(self, form):
        print("🚨 ОШИБКИ ФОРМЫ:", form.errors)
        print("📦 POST ДАННЫЕ:", self.request.POST)
        return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy("booking:index")


def logout(request):
    auth.logout(request)
    return redirect("booking:index")


# class EmailVerificationView(TitleMixin, TemplateView):
#     title = "Store - Confirm the email"
#     template_name = "users/email_verification.html"
#
#     def get(self, request, *args, **kwargs):
#         code = kwargs['code']
#         user = User.objects.get(email=kwargs['email'])
#         email_verifications = EmailVerification.objects.filter(user=user, code=code)
#         if email_verifications.exists() and not email_verifications.first().is_expired():
#             user.is_verified = True
#             user.save()
#             return super(EmailVerificationView, self).get(request, *args, **kwargs)
#         else:
#             return HttpResponseRedirect(reverse('products:index'))

class EmailVerificationView(View):
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        form = VerificationCodeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = VerificationCodeForm(request.POST)

        if form.is_valid():
            # Собираем введенные цифры
            digit1 = form.cleaned_data['digit1']
            digit2 = form.cleaned_data['digit2']
            digit3 = form.cleaned_data['digit3']
            digit4 = form.cleaned_data['digit4']
            user_code = digit1 + digit2 + digit3 + digit4

            # Используем filter() и проверяем, что запись одна
            email_verification = EmailVerification.objects.filter(user=request.user).first()

            if email_verification:
                if email_verification.code == user_code:
                    if email_verification.is_expired():
                        messages.error(request, "Your verification code has expired.")
                    else:
                        # Успешная верификация
                        messages.success(request, "Your email has been successfully verified!")
                        return redirect('booking:index')  # Перенаправление на домашнюю страницу
                else:
                    messages.error(request, "Invalid verification code.")
            else:
                messages.error(request, "No verification record found for this user.")

        return render(request, self.template_name, {'form': form})



class UserProfileView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = ProfileForm

    def form_valid(self, form):
        user = form.instance

        # Удаление изображения, если отмечен чекбокс
        if form.cleaned_data.get("delete_image"):
            user.image.delete(save=False)
            user.image = None

        # Если введен новый пароль → хешируем его
        new_password = form.cleaned_data.get("password")
        if new_password:
            user.password = make_password(new_password)

        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("users:profile", args=(self.object.id,))



def base(request):
    return render(request, "users/email_verification.html")


def landlord_reviews(request, pk):
    landlord = get_object_or_404(User, id=pk, is_landlord=True)
    apartments = Apartment.objects.filter(landlord=landlord)
    reviews = Review.objects.filter(apartment__in=apartments).select_related("author")

    return render(request, "profile/profile_landlord.html", {
        "user": landlord,
        "reviews": reviews,
        "apartments": apartments,
    })


def tenant_reviews(request, pk):
    tenant = get_object_or_404(User, id=pk, is_landlord=False)
    reviews = Review.objects.filter(author=tenant).select_related("apartment")
    apartments = tenant.favourites.all()
    print(apartments)
    return render(request, "profile/profile_tenant.html", {
        "user": tenant,
        "reviews": reviews,
        "apartments": apartments,
    })