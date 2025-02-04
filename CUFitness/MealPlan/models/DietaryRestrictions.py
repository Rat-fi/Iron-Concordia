from django.db import models
from django.contrib.auth.models import User

class DietaryRestrictions(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'dietary_restrictions')
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
