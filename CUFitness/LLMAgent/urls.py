from django.urls import path
from . import views

app_name = 'LLMAgent'  # This should match what's used in templates

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('generate_plan/', views.generate_fitness_plan, name='generate_plan'),
]