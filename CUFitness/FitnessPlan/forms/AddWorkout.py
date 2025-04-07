from django import forms
from ..models.AddWorkout import WorkoutPlan, Exercise

class WorkoutForm(forms.ModelForm):
    exercise = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Included Exercises"
    )

    class Meta:
        model = WorkoutPlan
        fields = ['workout_name', 'duration', 'calories', 'description', 'intensity_level', 'category', 'exercise']
        widgets = {
            'workout_name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'intensity_level': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
