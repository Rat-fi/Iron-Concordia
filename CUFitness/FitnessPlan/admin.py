from django.contrib import admin
from .models.AddWorkout import Exercise, WorkoutPlan


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')
    search_fields = ('name',)

@admin.register(WorkoutPlan)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('workout_name', 'duration', 'calories', 'description', 'intensity_level', 'category')
    list_filter = ('workout_name', 'duration', 'calories', 'intensity_level', 'category')
    search_fields = ('workout_name',)
