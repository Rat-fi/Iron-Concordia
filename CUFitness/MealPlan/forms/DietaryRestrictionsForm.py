from django import forms
from ..models.DietaryRestrictions import DietaryRestrictions

class DietaryRestrictionsForm(forms.ModelForm):
    class Meta:
        model = DietaryRestrictions
        fields = [
            'is_vegetarian', 'is_vegan', 'is_gluten_Free', 'is_lactose_Free', 
            'is_nut_Free', 'is_shellfish_Free', 'is_soy_free', 'is_egg_free',
            'is_pork_free', 'is_beef_free', 'is_fish_free', 'is_poultry_free'
            ]
