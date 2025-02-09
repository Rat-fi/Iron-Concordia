from django.contrib import admin
from .models.MealPlan_Searchbar import MealplanSearchbar
from .models.Budget import BudgetMeal
from .models.DietaryRestrictions import DietaryRestrictions,DietaryRestrictions_MealPlan
from .models.QuickMeal import QuickMeal
from .models.CampusOptions import CampusOptions_Restaurant, CampusOptions_MenuItem

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

@admin.register(QuickMeal)
class QuickMealAdmin(admin.ModelAdmin):
    list_display = ('name', 'preparation_time', 'cooking_materials')
    search_fields = ('name', 'cooking_materials')
    list_filter = ('preparation_time',)

admin.site.register(MealplanSearchbar)
admin.site.register(BudgetMeal)

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'rating', 'latitude', 'longitude')

admin.site.register(CampusOptions_Restaurant, RestaurantAdmin)
admin.site.register(CampusOptions_MenuItem)
