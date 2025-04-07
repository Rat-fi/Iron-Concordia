from django.urls import path
from .views.MealPlan_Searchbar import MealPlan_Searchbar
from .views.DietaryRestrictions import set_dietary_restrictions 
from .views.DietaryRestrictions import meal_plan
from .views.CampusOptions import campus_options
from .views.NewCookUser import meal_instructions_list

urlpatterns = [
    path('set_dietary_restrictions/', set_dietary_restrictions, name='set_dietary_restrictions'),
    path('meal_plan/', meal_plan, name='meal_plan'),
    # path('', MealPlan_Searchbar, name='MealPlan_Searchbar_home'),
    path('search/', MealPlan_Searchbar, name='MealPlan_Searchbar'),
    path('campus_options/', campus_options, name='campus_options'),
    path('meal_instructions/', meal_instructions_list, name = 'newcookuser_list'),
]
