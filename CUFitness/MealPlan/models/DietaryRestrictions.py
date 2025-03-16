from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class DietaryRestrictions_MealPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    calories = models.PositiveIntegerField(help_text="Calories per serving")
    protein = models.FloatField(validators=[MinValueValidator(0)], help_text="Protein in grams")
    
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    contains_gluten = models.BooleanField(default=False)
    contains_lactose = models.BooleanField(default=False)
    contains_nuts = models.BooleanField(default=False)
    contains_shellfish = models.BooleanField(default=False)
    contains_soy = models.BooleanField(default=False)
    contains_eggs = models.BooleanField(default=False)
    contains_pork = models.BooleanField(default=False)
    contains_beef = models.BooleanField(default=False)
    contains_fish = models.BooleanField(default=False)
    contains_poultry = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class DietaryRestrictions(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'dietary_restrictions')
    meal_plans = models.ManyToManyField(DietaryRestrictions_MealPlan, blank=True)
    
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)  
    is_gluten_Free = models.BooleanField(default=False)    
    is_lactose_Free = models.BooleanField(default=False)   
    is_nut_Free = models.BooleanField(default=False)   
    is_shellfish_Free = models.BooleanField(default=False) 
    is_soy_free = models.BooleanField(default=False)
    is_egg_free = models.BooleanField(default=False)
    is_pork_free = models.BooleanField(default=False)
    is_beef_free = models.BooleanField(default=False)
    is_fish_free = models.BooleanField(default=False)
    is_poultry_free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Dietary Restrictions"

