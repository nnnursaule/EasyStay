from . import views
from django.urls import path

app_name = 'booking'
urlpatterns = [
    path("", views.ResidentialComplexListView.as_view(), name='index'),
    path("main/<int:pk>/", views.main_page, name='main'),
    path("complex/<int:pk>/", views.ResidentialComplexDetailView.as_view(), name="complex_detail"),
    path("share", views.share_with_others, name="share"),
]