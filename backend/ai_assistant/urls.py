from django.urls import path
from .views import AIAssistantView
from . import views
app_name = "ai_assistant"
urlpatterns = [
    path('chat/', AIAssistantView.as_view(), name='ai_chat'),
    path('assistant/', views.ai_assistant_template, name='ai_template'),
]
