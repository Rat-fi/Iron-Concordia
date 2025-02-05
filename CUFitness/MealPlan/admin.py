from django.contrib import admin
from .models.MealPlan_Searchbar import MealplanSearchbar
from .models.Budget import BudgetMeal

admin.site.register(MealplanSearchbar)
admin.site.register(BudgetMeal)
