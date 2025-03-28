# Generated by Django 5.1.5 on 2025-02-08 02:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MealPlan', '0007_quickmeal'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampusOptions_Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Restaurant Name')),
                ('address', models.TextField(verbose_name='Restaurant Address')),
                ('rating', models.FloatField(verbose_name='Restaurant Rating')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
            ],
        ),
        migrations.CreateModel(
            name='CampusOptions_MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Item Name')),
                ('category', models.CharField(choices=[('staple', 'Staple'), ('side', 'Side'), ('drink', 'Drink'), ('dessert', 'Dessert')], max_length=255, verbose_name='Category')),
                ('dietary_restrictions', models.CharField(choices=[('vegetarian', 'Vegetarian'), ('vegan', 'Vegan'), ('gluten_free', 'Gluten Free'), ('lactose_free', 'Lactose Free'), ('nut_free', 'Nut Free'), ('shellfish_free', 'Shellfish Free'), ('soy_free', 'Soy Free'), ('egg_free', 'Egg Free'), ('pork_free', 'Pork Free'), ('beef_free', 'Beef Free'), ('fish_free', 'Fish Free'), ('poultry_free', 'Poultry Free'), ('none', 'No Restrictions')], default='none', max_length=255, verbose_name='Dietary Restrictions')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Price')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='MealPlan.campusoptions_restaurant')),
            ],
        ),
    ]
