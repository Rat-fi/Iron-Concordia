from django.db import models

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
    description = models.TextField("Exercise Dexcription")
    duration = models.PositiveIntegerField("Duration (minutes)", default = 0)
    calories = models.PositiveIntegerField("Calories burned", default = 0)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name="exercises")
    intensity_level = models.CharField("Workout Intensity", max_length= 20, default="Unknown", choices=INTENSITY_CHOICES)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name', 'duration', 'intensity_level']

