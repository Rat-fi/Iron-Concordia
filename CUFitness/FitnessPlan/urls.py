from django.urls import path
from .views.AddWorkout import create_workout, workout_detail, workout_list, edit_workout
from .views.BrowseWorkout import browse_exercise_list, toggle_favorite
from .views.PersonalizedPlan import collect_user_info_view, view_plan_view, adjust_plan_view

urlpatterns = [
    path('create/', create_workout, name='workout-create'),
    path('workout/<int:pk>/', workout_detail, name='workout-detail'),
    path('edit_workout/<int:pk>/', edit_workout, name='workout-edit'),
    path('workouts/',workout_list, name='workout-list'),
    path('exercises/', browse_exercise_list, name='browse_exercise_list'),
    path('toggle-favorite/<int:exercise_id>/', toggle_favorite, name='toggle_favorite'),
    path('collect', collect_user_info_view, name='collect_user_info'),
    path('view', view_plan_view, name='view_plan'),
    path('adjust', adjust_plan_view, name='adjust_plan'),
]