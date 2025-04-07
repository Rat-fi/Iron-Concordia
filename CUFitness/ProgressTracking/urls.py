from django.urls import path
from . import views

urlpatterns = [
    
    path('setDailyFitnessGoals/', views.set_daily_fitness_goal, name='set_goals'),
    path('setMyGymGoals/', views.set_my_gym_goal, name='set_my_gym_goals'),
    path('trackExercise/', views.track_exercise, name='track_exercise'),
    path('awards/', views.my_awards, name='my_awards'),
    path('todayRecords/', views.today_exercise_records, name='today_exercise_records'),
    path('editRecord/<int:record_id>', views.edit_exercise_record, name='edit_exercise_record'),
    path('removeRecord/<int:record_id>', views.remove_exercise_record, name='remove_exercise_record'),
    path('dailySummary/', views.daily_summary, name='daily_summary'),
    path('weeklySummary/', views.weekly_summary, name='weekly_summary'),
    path('monthlySummary/', views.monthly_summary, name='monthly_summary'),
    path('historyActivity/', views.history_activity, name='history_activity'),

    path('progressTracking/', views.index),
    path('checkHistory/<int:id>/', views.checkHistoryData),
    # path("", views.index, name = "index"),
    path("<int:question_id>/", views.detail, name='detail'),
    path("<int:question_id>/results/", views.result, name="result"),
    path("<int:question_id>/vote/", views.vote, name="vote")
]