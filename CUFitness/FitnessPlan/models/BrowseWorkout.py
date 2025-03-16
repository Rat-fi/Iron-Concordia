from django.db import models
from django.conf import settings # import the settings to use the user model because the custom user model

class Category(models.Model):
    name = models.CharField("Category Name", max_length = 50, unique = True)

    def __str__(self):
        return self.name

class BrowseWorkout(models.Model):

    INTENSITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    name = models.CharField("Exercise Name",max_length=255)
    description = models.TextField("Exercise Description")
    duration = models.PositiveIntegerField("Duration (minutes)", default = 0)
    calories = models.PositiveIntegerField("Calories burned", default = 0)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name="exercises")
    intensity_level = models.CharField("Workout Intensity", max_length= 20, default="Unknown", choices=INTENSITY_CHOICES)
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name='favorite_exercises') # combine the exercises favorited by the user

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name', 'duration', 'intensity_level']

