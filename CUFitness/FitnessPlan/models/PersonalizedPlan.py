from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

    
class FitnessPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fitness_plans')
    plan_content = models.TextField("Personalized Fitness Plan Details")
    created_at = models.DateTimeField("Create Time",auto_now_add=True)
    updated_at = models.DateTimeField("Update Time", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Fitness Plan at {self.created_at}"


User = get_user_model()

class UserBodyInfo(models.Model):
    GOAL_CHOICES = [
    ('weight_loss', 'Weight Loss'),
    ('muscle_gain', 'Muscle Gain'),
    ('endurance', 'Endurance'),
    ('general_fitness', 'General Fitness'),
    ('flexibility', 'Flexibility'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='body_info')
    height = models.PositiveIntegerField(help_text="Height in centimeters")
    weight = models.PositiveIntegerField(help_text="Weight in kilograms")
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    fitness_goal = models.CharField(max_length=50, choices=GOAL_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s Body Info"
