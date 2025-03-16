from django.db import models

class QuickMeal(models.Model):
    name = models.CharField(max_length=255, verbose_name="Meal Name")
    preparation_time = models.PositiveIntegerField(verbose_name="Preparation Time (minutes)")
    cooking_materials = models.TextField(verbose_name="Cooking Materials")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name