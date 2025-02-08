from django.urls import path
from . import views

urlpatterns = [
    path('progressTracking/', views.index),
    path('setDailyFitnessGoals/', views.set_daily_fitness_goal, name='set_goals'),
    path('setMyGymGoals/', views.set_my_gym_goal, name='set_my_gym_goals'),
    path('checkHistory/<int:id>/', views.checkHistoryData),
    # path("", views.index, name = "index"),
    path("<int:question_id>/", views.detail, name='detail'),
    path("<int:question_id>/results/", views.result, name="result"),
    path("<int:question_id>/vote/", views.vote, name="vote")
]