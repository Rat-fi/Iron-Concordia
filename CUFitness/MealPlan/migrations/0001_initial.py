# Generated by Django 5.1.4 on 2025-01-31 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MealplanSearchbar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('Meat', 'Meat'), ('Vegetable', 'Vegetable'), ('Dietary Restrictions', 'Dietary Restrictions')], max_length=100)),
            ],
        ),
    ]
