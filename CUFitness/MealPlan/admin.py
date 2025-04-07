from django.contrib import admin
from .models.DietaryRestrictions import DietaryRestrictions, DietaryRestrictions_MealPlan
from .models.CampusOptions import CampusOptions_Restaurant, CampusOptions_MenuItem

@admin.register(DietaryRestrictions_MealPlan)
class DietaryRestrictionsMealPlanAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'calories', 'protein', 'price', 'prepare_time', 'difficulty',
        'is_vegetarian', 'is_vegan', 'contains_gluten', 'contains_lactose'
    )
    list_filter = (
        'difficulty',
        'is_vegetarian', 'is_vegan',
        'contains_gluten', 'contains_lactose', 'contains_nuts', 'contains_shellfish',
        'contains_soy', 'contains_eggs', 'contains_pork', 'contains_beef',
        'contains_fish', 'contains_poultry'
    )
    search_fields = ('name', 'description', 'steps')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'calories', 'protein', 'price', 'prepare_time', 'difficulty', 'steps')
        }),
        ('Dietary Properties', {
            'fields': (
                'is_vegetarian', 'is_vegan',
                'contains_gluten', 'contains_lactose', 'contains_nuts', 'contains_shellfish',
                'contains_soy', 'contains_eggs', 'contains_pork', 'contains_beef',
                'contains_fish', 'contains_poultry'
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(DietaryRestrictions)
class DietaryRestrictionsAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'is_vegetarian', 'is_vegan', 'is_gluten_Free', 'is_lactose_Free',
        'is_nut_Free', 'is_shellfish_Free', 'is_soy_free', 'is_egg_free'
    )
    list_filter = (
        'is_vegetarian', 'is_vegan', 'is_gluten_Free', 'is_lactose_Free',
        'is_nut_Free', 'is_shellfish_Free', 'is_soy_free', 'is_egg_free',
        'is_pork_free', 'is_beef_free', 'is_fish_free', 'is_poultry_free'
    )
    search_fields = ('user__username',)
    filter_horizontal = ('meal_plans',)


@admin.register(CampusOptions_Restaurant)
class CampusOptionsRestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'rating', 'latitude', 'longitude')
    search_fields = ('name', 'address')


@admin.register(CampusOptions_MenuItem)
class CampusOptionsMenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'category', 'price', 'dietary_restrictions')
    list_filter = ('category',)
    search_fields = ('name', 'restaurant__name', 'dietary_restrictions')
