from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)

class Choise(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class DailyFitnessGoal(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    standing_time = models.FloatField(default=0)      
    exercise_minutes = models.PositiveIntegerField(default=0)  
    walking_distance = models.FloatField(default=0)     
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Daily Fitness Goal"
    
class GymGoal(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cardio = models.FloatField(default=0)
    weight_lifting = models.FloatField(default=0)
    yoga = models.FloatField(default=0)
    pilates = models.FloatField(default=0)
    hiit = models.FloatField(default=0)
    cycling = models.FloatField(default=0)
    swimming = models.FloatField(default=0)
    running = models.FloatField(default=0)
    rowing = models.FloatField(default=0)
    boxing = models.FloatField(default=0)
    dancing = models.FloatField(default=0)
    strength_training = models.FloatField(default=0)
    crossfit = models.FloatField(default=0)
    stretching = models.FloatField(default=0)
    elliptical_trainer = models.FloatField(default=0)
    goal_date = models.DateField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Gym Goals"

exercises = [
    ('cardio', 'Cardio'),
    ('weight_lifting', 'Weight Lifting'),
    ('yoga', 'Yoga'),
    ('pilates', 'Pilates'),
    ('hiit', 'HIIT'),
    ('cycling', 'Cycling'),
    ('swimming', 'Swimming'),
    ('running', 'Running'),
    ('rowing', 'Rowing'),
    ('boxing', 'Boxing'),
    ('dancing', 'Dancing'),
    ('strength_training', 'Strength Training'),
    ('crossfit', 'CrossFit'),
    ('stretching', 'Stretching'),
    ('elliptical_trainer', 'Elliptical Trainer'),
]

class ExerciseSession(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise_type = models.CharField(max_length=50, choices=exercises)
    exercise_time = models.PositiveIntegerField(help_text="Exercise duration in seconds")
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise_type} for {self.exercise_time} sec on {self.recorded_at}"
    

class FitnessActivity(models.Model):
    EXERCISE_CHOICES = [
        ('cardio', 'Cardio'),
        ('weight_lifting', 'Weight Lifting'),
        ('yoga', 'Yoga'),
        ('pilates', 'Pilates'),
        ('hiit', 'HIIT'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('running', 'Running'),
        ('rowing', 'Rowing'),
        ('boxing', 'Boxing'),
        ('dancing', 'Dancing'),
        ('strength_training', 'Strength Training'),
        ('crossfit', 'CrossFit'),
        ('stretching', 'Stretching'),
        ('elliptical_trainer', 'Elliptical Trainer'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    exercise_type = models.CharField(
        max_length=30,
        choices=EXERCISE_CHOICES,
        help_text="Type of exercise."
    )
    recommended_duration_minutes = models.PositiveIntegerField(
        help_text="Recommended duration (in minutes) for the activity."
    )
    calories_per_minute = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Estimated calories burned per minute."
    )
    difficulty_level = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        help_text="Difficulty level of the activity."
    )
    target_category = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Primary target category (e.g., cardiovascular, strength, flexibility)."
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the activity."
    )

    def __str__(self):
        return self.get_exercise_type_display()

    class Meta:
        db_table = 'fitness_activity'