from django import forms
from ..models.DietaryRestrictions import DietaryRestrictions,DietaryRestrictions_MealPlan

class DietaryRestrictionsForm(forms.ModelForm):
    meal_plans = forms.ModelMultipleChoiceField(
        queryset = DietaryRestrictions_MealPlan.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        help_text = "Select meal plans that fit your dietary restrictions."
    )
    class Meta:
        model = DietaryRestrictions
        fields = [
            'is_vegetarian', 'is_vegan', 'is_gluten_Free', 'is_lactose_Free', 
            'is_nut_Free', 'is_shellfish_Free', 'is_soy_free', 'is_egg_free',
            'is_pork_free', 'is_beef_free', 'is_fish_free', 'is_poultry_free'
            ]
