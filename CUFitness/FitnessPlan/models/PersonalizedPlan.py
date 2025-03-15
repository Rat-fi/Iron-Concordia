from django.db import models
from django.conf import settings

    
class FitnessPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fitness_plans')
    plan_content = models.TextField("Personalized Fitness Plan Details")
    created_at = models.DateTimeField("Create Time",auto_now_add=True)
    updated_at = models.DateTimeField("Update Time", auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Fitness Plan at {self.created_at}"
