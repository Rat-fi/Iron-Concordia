from django.urls import path
from .views.AddWorkout import create_workout, workout_detail, workout_list
from .views.BrowseWorkout import browse_category_list, browse_exercise_list, toggle_favorite, favorite_list

urlpatterns = [
    path('create/', create_workout, name='workout-create'),
    path('workout/<int:pk>/', workout_detail, name='workout-detail'),
    path('workouts/',workout_list, name='workout-list'),
    path('browse_categories/', browse_category_list, name='browse_category_list'),
    path('browse_exercises/', browse_exercise_list, name='browse_exercise_list'),
    path('toggle_favorite/<int:exercise_id>/', toggle_favorite, name='toggle_favorite'),
    path('favorites/', favorite_list, name='favorite_list'),
]