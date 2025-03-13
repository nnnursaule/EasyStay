from django.urls import path
from . import views
app_name = "users"
urlpatterns = [
    path('registration/', views.UserCreationView.as_view(), name='registration'),
    path("login", views.UserLoginView.as_view(), name='login'),
    path("logout", views.logout, name='logout'),
    path('verify/<str:email>/<uuid:code>/', views.EmailVerificationView.as_view(), name='verify')
]
