from django.urls import path
from .views.DietaryRestrictions import ( set_dietary_restrictions, create_meal_plan)
from .views.CampusOptions import campus_options
from .views.MealPlanSearch import search_meal_plans

urlpatterns = [
    path('set_dietary_restrictions/', set_dietary_restrictions, name='set_dietary_restrictions'),
    path('campus_options/', campus_options, name='campus_options'),
    path('create_meal_plan/', create_meal_plan, name='create_meal_plan'),
    path('search_meal_plans/', search_meal_plans, name='search_meal_plans'),
]
