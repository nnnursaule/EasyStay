from . import views
from django.urls import path

app_name = 'booking'
urlpatterns = [
    path("", views.ResidentalComplexListView.as_view(), name='index'),
    path("main/<int:pk>/", views.main_page, name='main'),
    path("apartment/<int:pk>/", views.ApartmentDetailView.as_view(), name="apartment_detail"),
    path("share/<int:apartment_id>/", views.share_with_others, name="share"),
    path("landlord_apartments/<int:pk>/", views.landlord_apartments, name="landlord_apartments"),
    path('apartments/<int:pk>/new/', views.ApartmentCreateView.as_view(), name='apartment_create'),
    path('apartments/<int:pk>/edit/', views.ApartmentUpdateView.as_view(), name='apartment_update'),
    path('apartments/<int:pk>/delete/', views.ApartmentDeleteView.as_view(), name='apartment_delete'),
    path('delete_apartment/<int:pk>/', views.delete_apartment, name='delete_apartment'),
    path('favourites/remove/<int:apartment_id>/', views.remove_from_favourites, name='remove_from_favourites'),
    path('favourites/', views.favourites_view, name='favourites'),
    path('favourite/<int:apartment_id>/', views.toggle_favourite, name='toggle_favourite'),
    path('favourites/add/<int:apartment_id>/', views.add_to_favourites, name='add_to_favourites'),
    path('residential-complex/<int:pk>/', views.ResidentialComplexView.as_view(), name='complex_details'),
    path('complaint/<int:apartment_id>/', views.submit_complaint, name='submit_complaint'),
    path('submit-site-feedback/', views.submit_site_feedback, name='submit_site_feedback'),
    path('apartments/<int:apartment_id>/review/', views.submit_apartment_review, name='submit_apartment_review'),
    path('apartment/<int:apartment_id>/booking/', views.confirm_booking, name='confirm_booking'),
    path('success/<int:apartment_id>/', views.successful_after_booking, name='success'),
    path('promotion_success/<int:apartment_id>/', views.promote_success, name='promotion_success'),
    path('apartment/<int:apartment_id>/promotion/', views.choose_promotion_plan, name='choose_promotion_plan'),
    path('promote/<int:apartment_id>/pay/', views.create_checkout_session, name='create_checkout'),
    path('promote/cancel/', views.promote_cancel, name='promotion_cancel'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('apartments/<int:apartment_id>/reviews/', views.submit_review, name='submit_review'),


]