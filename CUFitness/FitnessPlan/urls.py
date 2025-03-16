from django.urls import path
from .views.AddWorkout import create_workout, workout_detail, workout_list, edit_workout
from .views.BrowseWorkout import browse_category_list, browse_exercise_list, toggle_favorite, favorite_list
from .views.PersonalizedPlan import collect_user_info_view, view_plan_view, adjust_plan_view

urlpatterns = [
    path('create/', create_workout, name='workout-create'),
    path('workout/<int:pk>/', workout_detail, name='workout-detail'),
    path('edit_workout/<int:pk>/', edit_workout, name='workout-edit'),
    path('workouts/',workout_list, name='workout-list'),
    path('browse_categories/', browse_category_list, name='browse_category_list'),
    path('browse_exercises/', browse_exercise_list, name='browse_exercise_list'),
    path('toggle_favorite/<int:exercise_id>/', toggle_favorite, name='toggle_favorite'),
    path('favorites/', favorite_list, name='favorite_list'),
    path('collect', collect_user_info_view, name='collect_user_info'),
    path('view', view_plan_view, name='view_plan'),
    path('adjust', adjust_plan_view, name='adjust_plan'),
]