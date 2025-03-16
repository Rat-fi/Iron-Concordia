from django.db import models
from django.core.validators import MinValueValidator

class CampusOptions_Restaurant(models.Model):
    name = models.CharField(max_length=255, verbose_name="Restaurant Name")
    address = models.TextField(verbose_name="Restaurant Address")
    rating = models.FloatField(verbose_name="Restaurant Rating", default=0.0, validators=[MinValueValidator(0)])
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")

    def __str__(self):
        return self.name
    
    

class CampusOptions_MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('staple', 'Staple'),
        ('side', 'Side'),
        ('drink', 'Drink'),
        ('dessert', 'Dessert'),
    ]

    DIETARY_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('gluten_free', 'Gluten Free'),
        ('lactose_free', 'Lactose Free'),
        ('nut_free', 'Nut Free'),
        ('shellfish_free', 'Shellfish Free'),
        ('soy_free', 'Soy Free'),
        ('egg_free', 'Egg Free'),
        ('pork_free', 'Pork Free'),
        ('beef_free', 'Beef Free'),
        ('fish_free', 'Fish Free'),
        ('poultry_free', 'Poultry Free'),
        ('none', 'No Restrictions'),
    ]

    restaurant = models.ForeignKey(CampusOptions_Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255, verbose_name="Item Name")
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, verbose_name="Category")
    dietary_restrictions = models.CharField(max_length=255, choices=DIETARY_CHOICES, default = 'none', verbose_name="Dietary Restrictions")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Price", validators=[MinValueValidator(0)])
#    calories = models.IntegerField(verbose_name="Calories")

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"