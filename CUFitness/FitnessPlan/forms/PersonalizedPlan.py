from django import forms
from ..models.PersonalizedPlan import UserBodyInfo  # Adjust the import if needed

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserBodyInfo
        fields = ['age', 'weight', 'height', 'gender', 'fitness_goal']
        labels = {
            'fitness_goal': 'Fitness Goal',
        }
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'fitness_goal': forms.Select(attrs={'class': 'form-control'}),
        }
