from django.db import models

class MealplanSearchbar(models.Model):
    Category_choices = [
        ('Meat', 'Meat'),
        ('Vegetable', 'Vegetable'),
        ('Dietary Restrictions', 'Dietary Restrictions'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=Category_choices)

    def __str__(self):
        return self.name
   