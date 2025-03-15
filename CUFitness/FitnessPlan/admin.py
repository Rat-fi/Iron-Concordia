from django.contrib import admin
from .models.AddWorkout import Exercise, WorkoutPlan
from .models.BrowseWorkout import Category, BrowseWorkout
from .models.PersonalizedPlan import FitnessPlan


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

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(BrowseWorkout)
class BrowseWorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'duration', 'calories', 'category', 'intensity_level')
    list_filter = ('name', 'description', 'duration', 'calories', 'category', 'intensity_level')
    search_fields = ('name',)


@admin.register(FitnessPlan)
class FitnessPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_content', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at', 'updated_at')
    search_fields = ('user',)