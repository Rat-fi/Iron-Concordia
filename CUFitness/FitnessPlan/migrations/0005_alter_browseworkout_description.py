# Generated by Django 5.1.5 on 2025-03-09 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitnessPlan', '0004_browseworkout_favorited_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='browseworkout',
            name='description',
            field=models.TextField(verbose_name='Exercise Description'),
        ),
    ]
