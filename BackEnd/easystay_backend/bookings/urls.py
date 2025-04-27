from . import views
from django.urls import path

app_name = 'booking'
urlpatterns = [
    path("", views.ApartmentListView.as_view(), name='index'),
    path("main/<int:pk>/", views.main_page, name='main'),
    path("apartment/<int:pk>/", views.ApartmentDetailView.as_view(), name="apartment_detail"),
    path("share/<int:apartment_id>/", views.share_with_others, name="share"),
    path("landlord_apartments/<int:pk>/", views.landlord_apartments, name="landlord_apartments"),
    path('apartments/new/', views.ApartmentCreateView.as_view(), name='apartment_create'),
    path('apartments/<int:pk>/edit/', views.ApartmentUpdateView.as_view(), name='apartment_update'),
    path('apartments/<int:pk>/delete/', views.ApartmentDeleteView.as_view(), name='apartment_delete'),
    path('delete_apartment/<int:pk>/', views.delete_apartment, name='delete_apartment'),
    path('favourites/remove/<int:apartment_id>/', views.remove_from_favourites, name='remove_from_favourites'),
    path('favourites/', views.favourites_view, name='favourites'),
    path('favourite/<int:apartment_id>/', views.toggle_favourite, name='toggle_favourite'),
    path('favourites/add/<int:apartment_id>/', views.add_to_favourites, name='add_to_favourites'),

]