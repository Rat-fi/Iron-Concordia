from django.db import models

class BudgetMeal(models.Model):
    name = models.CharField(max_length = 255)
    price = models.DecimalField(max_digits = 6, decimal_places = 2)

    class Meta:
        db_table = 'budget_meal'

    def __str__(self):
        return self.name