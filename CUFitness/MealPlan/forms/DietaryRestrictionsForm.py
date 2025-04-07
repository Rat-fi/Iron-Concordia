from django import forms
from ..models.DietaryRestrictions import DietaryRestrictions_MealPlan
from ..models.DietaryRestrictions import DietaryRestrictions

class DietaryRestrictionsMealPlanForm(forms.ModelForm):
    class Meta:
        model = DietaryRestrictions_MealPlan
        fields = [
            'name', 'description', 'calories', 'protein', 'price', 'prepare_time',
            'difficulty', 'steps',
            'is_vegetarian', 'is_vegan',
            'contains_gluten', 'contains_lactose', 'contains_nuts', 'contains_shellfish',
            'contains_soy', 'contains_eggs', 'contains_pork', 'contains_beef',
            'contains_fish', 'contains_poultry'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'prepare_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'steps': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        dietary_fields = [
            'is_vegetarian', 'is_vegan', 'contains_gluten', 'contains_lactose', 
            'contains_nuts', 'contains_shellfish', 'contains_soy', 'contains_eggs',
            'contains_pork', 'contains_beef', 'contains_fish', 'contains_poultry'
        ]
        
        for field in dietary_fields:
            self.fields[field].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
            self.fields[field].label = self.fields[field].label.replace('_', ' ').capitalize()


class DietaryRestrictionsForm(forms.ModelForm):
    class Meta:
        model = DietaryRestrictions
        fields = [
            'is_vegetarian', 'is_vegan', 'is_gluten_Free', 'is_lactose_Free',
            'is_nut_Free', 'is_shellfish_Free', 'is_soy_free', 'is_egg_free',
            'is_pork_free', 'is_beef_free', 'is_fish_free', 'is_poultry_free',
            'meal_plans'
        ]
        widgets = {
            'meal_plans': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        dietary_fields = [
            'is_vegetarian', 'is_vegan', 'is_gluten_Free', 'is_lactose_Free',
            'is_nut_Free', 'is_shellfish_Free', 'is_soy_free', 'is_egg_free',
            'is_pork_free', 'is_beef_free', 'is_fish_free', 'is_poultry_free',
        ]

        for field in dietary_fields:
            self.fields[field].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
            self.fields[field].label = self.fields[field].label.replace('_', ' ').replace('is ', '').capitalize()

        self.fields['meal_plans'].label = "Select Meal Plans"