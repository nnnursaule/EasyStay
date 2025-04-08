from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = "users"
urlpatterns = [
    path('registration/', views.UserCreationView.as_view(), name='registration'),
    path("login", views.UserLoginView.as_view(), name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page="users:logout_page"), name="logout"),
    path("logout_page/", views.logout_page, name="logout_page"),  # Страница подтверждения выхода
    path('verify-email', views.EmailVerificationView.as_view(), name='verify-email'),
    path("landlord_profile_info/<int:pk>/", views.landlord_reviews, name='landlord_profile'),
    path("tenant_profile_info/<int:pk>/", views.tenant_reviews, name='tenant_profile'),
    path("edit_profile/<int:pk>/", views.UserProfileView.as_view(), name='edit_profile'),
    path("base", views.base, name="base"),
    path("password-reset/", views.password_reset_request, name="password_reset_request"),
    path("digit_code/", views.verify_code, name='digit_code'),
    path("set_new_password/<uidb64>/<token>/", views.SetNewPasswordView.as_view(), name='set_new_password'),
    path("success/", views.successful_view, name="success"),


]
