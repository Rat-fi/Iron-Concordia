from django import forms
from ..models.AddWorkout import WorkoutPlan, Exercise

class WorkoutForm(forms.ModelForm):
    exercise = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(), 
        widget=forms.CheckboxSelectMultiple,
        required=True)
    class Meta:
        model = WorkoutPlan
        fields = ['workout_name', 'duration', 'calories', 'description', 'intensity_level', 'category', 'exercise']