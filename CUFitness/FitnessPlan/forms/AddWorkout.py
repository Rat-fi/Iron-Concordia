from django import forms
from ..models.AddWorkout import WorkoutPlan, Exercise

class WorkoutForm(forms.ModelForm):
    exercise = forms.ModelMultipleChoiceField( # Using to select multiple exercises
        queryset=Exercise.objects.all(), # Query all exercises
        widget=forms.CheckboxSelectMultiple, # Using checkbox to select multiple exercises
        required=True) # At least one exercise
    class Meta:
        model = WorkoutPlan
        fields = ['workout_name', 'duration', 'calories', 'description', 'intensity_level', 'category', 'exercise']