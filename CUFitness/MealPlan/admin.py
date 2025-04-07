from django.contrib import admin
from .models.MealPlan_Searchbar import MealplanSearchbar
from .models.DietaryRestrictions import DietaryRestrictions,DietaryRestrictions_MealPlan
from .models.CampusOptions import CampusOptions_Restaurant, CampusOptions_MenuItem
from .models.NewCookUser import MealInstructions

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

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'rating', 'latitude', 'longitude')

admin.site.register(CampusOptions_Restaurant, RestaurantAdmin)
admin.site.register(CampusOptions_MenuItem)

@admin.register(MealInstructions)
class MealInstructionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'price', 'prepare_time', 'calories', 'protein')
    search_fields = ('name', 'dietary_restrictions')