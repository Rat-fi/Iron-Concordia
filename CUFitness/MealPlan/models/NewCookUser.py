from django.db import models
from django.core.validators import MinValueValidator

class MealInstructions(models.Model):
    name = models.CharField(max_length=255)

    DIFFICULTY_CHOICES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)

    dietary_restrictions = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated dietary restrictions. (e.g., vegan, gluten-free)"
        )
    
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    prepare_time = models.PositiveIntegerField(help_text="Preparation time in minutes.")

    calories = models.PositiveIntegerField()

    protein = models.PositiveIntegerField(help_text="Protein content in grams")

    steps = models.TextField(help_text = "Step-by-step meal preparation instructions")

    def __str__(self):
        return self.name
    