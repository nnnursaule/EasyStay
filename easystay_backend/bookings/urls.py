from . import views
from django.urls import path

app_name = 'booking'
urlpatterns = [
    path("", views.index, name='index'),

]