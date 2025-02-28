from django.urls import path
from .views.AddWorkout import create_workout, workout_detail, workout_list

urlpatterns = [
    path('create/', create_workout, name='workout-create'),
    path('workout/<int:pk>/', workout_detail, name='workout-detail'),
    path('workouts/',workout_list, name='workout-list'),
]