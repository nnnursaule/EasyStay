from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from . forms import UserRegistrationForm, UserLoginForm


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
    success_url = reverse_lazy("users:login")
    success_message = "Congratulations, You successfully registered!"
    title = "Store - Registration"

    def form_valid(self, form):
        print("Form is valid!")  # Проверяем, срабатывает ли метод
        return super().form_valid(form)

    def form_invalid(self, form):
        print("🚨 FORM ERRORS:", form.errors)  # Выведет ошибки формы в консоль
        print("📦 POST DATA:", self.request.POST)  # Покажет, какие данные пришли
        return super().form_invalid(form)



class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy("booking:index")


def logout(request):
    auth.logout(request)
    return redirect("booking:index")