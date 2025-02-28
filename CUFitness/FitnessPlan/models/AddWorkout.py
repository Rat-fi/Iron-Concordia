from django.db import models

class Exercise(models.Model):
    INTENSITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('Cardio', 'Cardio'),
        ('Strength', 'Strength'),
        ('Flexibility', 'Flexibility'),
        ('Balance', 'Balance'),
    ]

    name = models.CharField("Exercise Name",max_length = 255)
    description = models.TextField("Exercise Description")
    duration = models.PositiveIntegerField("Duration (minutes)",default=0)
    calories = models.PositiveIntegerField("Calories burned",default=0)
    intensity_level = models.CharField("Workout Intensity", max_length=10, default="Unknown", choices=INTENSITY_CHOICES)
    category = models.CharField("Workout Category", max_length=20, default="Unknown", choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
    

class WorkoutPlan(models.Model):
    INTENSITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('Cardio', 'Cardio'),
        ('Strength', 'Strength'),
        ('Flexibility', 'Flexibility'),
        ('Balance', 'Balance'),
    ]

    workout_name = models.CharField("Workout Name", max_length = 255)
    description = models.TextField("Workout Description")
    duration = models.PositiveIntegerField("Duration (minutes)",default=0)
    calories = models.PositiveIntegerField("Calories burned",default=0)
    intensity_level = models.CharField("Workout Intensity", max_length=10, default="Unknown", choices=INTENSITY_CHOICES)
    category = models.CharField("Workout Category", max_length=20, default="Unknown", choices=CATEGORY_CHOICES)
    exercise = models.ManyToManyField(Exercise, verbose_name="Exercises")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return self.workout_name
    
