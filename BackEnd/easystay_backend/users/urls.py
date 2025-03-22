from django.urls import path
from . import views
app_name = "users"
urlpatterns = [
    path('registration/', views.UserCreationView.as_view(), name='registration'),
    path("login", views.UserLoginView.as_view(), name='login'),
    path("logout", views.logout, name='logout'),
    path('verify-email', views.EmailVerificationView.as_view(), name='verify-email'),
    path("profile/<int:pk>/", views.UserProfileView.as_view(), name='profile'),
    path("base", views.base, name="base"),
]
