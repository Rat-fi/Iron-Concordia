from django import forms
from django.core.validators import MinValueValidator

class UserInfoForm(forms.Form):
    GENDER_CHOICES =[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    GOAL_CHOICES = [
        ('Lose Weight', 'Lose Weight'),
        ('Gain Muscle', 'Gain Muscle'),
        ('Stay Fit', 'Stay Fit'),
    ]

    weight = forms.FloatField(label='Weight (kg)', required=True, validators=[MinValueValidator(0)])
    height = forms.FloatField(label='Height (cm)', required=True, validators=[MinValueValidator(0)])
    age = forms.IntegerField(label='Age', required=True, validators=[MinValueValidator(0)])
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, required=True)
    goal = forms.ChoiceField(label='Goal', choices=GOAL_CHOICES, required=True)
    dietary_restrictions = forms.CharField(label='Dietary Restrictions', required=False)