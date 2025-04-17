from . import views
from django.urls import path

app_name = 'booking'
urlpatterns = [
    path("", views.ResidentialComplexListView.as_view(), name='index'),
    path("main/<int:pk>/", views.main_page, name='main'),
    path("complex/<int:pk>/", views.ResidentialComplexDetailView.as_view(), name="complex_detail"),
    path("share", views.share_with_others, name="share"),
    path("landlord_apartments/<int:pk>/", views.landlord_apartments, name="landlord_apartments"),
    path('apartments/new/', views.ApartmentCreateView.as_view(), name='apartment_create'),
    path('apartments/<int:pk>/edit/', views.ApartmentUpdateView.as_view(), name='apartment_update'),
    path('apartments/<int:pk>/delete/', views.ApartmentDeleteView.as_view(), name='apartment_delete'),
    path('delete_apartment/<int:pk>/', views.delete_apartment, name='delete_apartment'),
]