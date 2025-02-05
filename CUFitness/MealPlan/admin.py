from django.contrib import admin
from .models.MealPlan_Searchbar import MealplanSearchbar
from .models.Budget import BudgetMeal
from .models.DietaryRestrictions import DietaryRestrictions,DietaryRestrictions_MealPlan

@admin.register(DietaryRestrictions_MealPlan)
class DietaryRestrictionsMealPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein', 'is_vegetarian', 'is_vegan')
    list_filter = ('is_vegetarian', 'is_vegan', 'contains_gluten', 'contains_lactose')
    search_fields = ('name', 'description')

@admin.register(DietaryRestrictions)
class DietaryRestrictionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_vegetarian', 'is_vegan', 'is_gluten_Free', 'is_lactose_Free')
    list_filter = ('is_vegetarian', 'is_vegan', 'is_gluten_Free', 'is_lactose_Free')
    search_fields = ('user__username',)
    filter_horizontal = ('meal_plans',)

admin.site.register(MealplanSearchbar)
admin.site.register(BudgetMeal)
