from . import views
from django.urls import path

app_name = 'booking'
urlpatterns = [
    path("", views.ResidentialComplexListView.as_view(), name='index'),
    path("complex/<int:pk>/", views.ResidentialComplexDetailView.as_view(), name="complex_detail"),
]