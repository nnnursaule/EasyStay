from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model, login, update_session_auth_hash, logout
from . forms import UserRegistrationForm, UserLoginForm, ProfileForm, VerificationCodeForm, PasswordResetRequestForm, ResetPasswordForm
from .models import  User, EmailVerification
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from datetime import timedelta
from bookings.models import Review, Apartment
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache

from django.http import Http404
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes



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

    def get_success_url(self):
        # Получаем id текущего пользователя
        pk = self.request.user.id
        # Редиректим на страницу с этим pk
        return reverse_lazy("booking:main", kwargs={'pk': pk})

    def form_invalid(self, form):
        # Добавляем ошибку, если аутентификация не удалась
        messages.error(self.request, "Username or password incorrect")
        return super().form_invalid(form)

def logout_page(request):
    if request.method == "POST":
        print("POOOOOOST")
        logout(request)
        return redirect("booking:index")  # После выхода перенаправить на главную
    return render(request, "users/logout.html", {
        "user": request.user
    })


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



class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile/edit_profile_landlord.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user  # Возвращаем текущего пользователя

    def form_valid(self, form):
        print("VALIIIIIDDDDDD")
        user = form.save(commit=False)

        # Удаление изображения, если отмечен чекбокс
        if form.cleaned_data.get("delete_image"):
            user.image.delete(save=False)
            user.image = None

        # Если введен новый пароль, обновляем сессию
        if form.cleaned_data.get("new_password"):
            update_session_auth_hash(self.request, user)

        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        print("SUCCESSSSSS")
        return reverse_lazy("users:edit_profile", args=(self.object.id,))

    def form_invalid(self, form):
        print("INVALID FORM")  # Должно появиться в консоли, если форма невалидна
        print(form.errors)  # Выведет ошибки формы
        return self.render_to_response(self.get_context_data(form=form))





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
    return render(request, "profile/profile_tenant.html", {
        "user": tenant,
        "reviews": reviews,
    })


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)

            # Генерация 4-значного кода
            reset_code = str(random.randint(1000, 9999))

            # Сохранение кода в кэше на 5 минут
            cache.set(f"reset_code_{email}", reset_code, timeout=300)
            print(f"Saved code {reset_code} for {email}")  # Отладка

            # Отправка кода на email
            send_mail(
                "Password Reset Code",
                f"Your verification code: {reset_code}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            print(f"Generated uidb64: {uidb64}, token: {token}")

            # Сохранение в сессию
            request.session["uidb64"] = uidb64
            request.session["token"] = token
            request.session["reset_email"] = email
            request.session.modified = True

            return redirect(reverse("users:digit_code"))

    else:
        form = PasswordResetRequestForm()

    return render(request, "users/forgot.html", {"form": form})

def verify_code(request):
    if request.method == "POST":
        print("AAAAAAA")
        print("POST data:", request.POST)
        code = request.POST.get("code1") + request.POST.get("code2") + request.POST.get("code3") + request.POST.get("code4")
        email = request.session.get("reset_email")

        if not email:
            messages.error(request, "Сессия истекла. Попробуйте снова.")
            return redirect("users:forgot_password")

        stored_code = cache.get(f"reset_code_{email}")
        print(f"Email: {email}")
        print(f"Entered code: {code}")
        print(f"Stored code: {stored_code}")

        if stored_code and code == stored_code:
            print("BBBBBB")
            uidb64 = request.session.get('uidb64')
            token = request.session.get('token')

            if uidb64 and token:
                print("CCCCCCCC")
                return redirect('users:set_new_password', uidb64=uidb64, token=token)
            else:
                print("DDDDDD")
                messages.error(request, "Ссылка для сброса пароля недействительна или истекла.")
                return redirect('users:forgot_password')
        else:
            print("EEEEEEE")
            messages.error(request, "Неверный код подтверждения.")
            return redirect("users:digit_code")

    uidb64 = request.session.get('uidb64')
    token = request.session.get('token')
    return render(request, "users/password_verification.html", {'uidb64': uidb64, 'token': token})

class SetNewPasswordView(View):
    template_name = "users/new_password.html"

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = ResetPasswordForm(user=user)  # Передаём пользователя в форму
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, "The password reset link is invalid or expired.")
            return redirect('users:password_reset_request')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            print("STTOOOOOOPPPP")
            form = ResetPasswordForm(user, request.POST)  # Передаём пользователя + данные формы
            if form.is_valid():
                print("yessss")
                form.save()  # `SetPasswordForm` уже содержит метод `save()`
                messages.success(request, "Your password has been successfully reset!")
                return redirect('users:success')
            else:
                print("nooo")
                print(form.errors)
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, "The password reset link is invalid or expired.")
            return redirect('users:password_reset_request')



def successful_view(request):
    return render(request, "users/successfull.html")


def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    author = review.author  # Сохраняем объект автора до удаления
    review.delete()

    if author.is_landlord:
        return redirect('users:landlord_profile', pk=author.id)
    else:
        return redirect('users:tenant_profile', pk=author.id)

class ReviewUpdateView(UpdateView):
    model = Review
    fields = ['text']  # только текст можно изменить
    template_name = 'profile/edit_review.html'

    def get_success_url(self):
        if self.object.author.is_landlord:
            return reverse('users:landlord_profile', kwargs={'pk': self.object.author.id})
        else:
            return reverse('users:tenant_profile', kwargs={'pk': self.object.author.id})


