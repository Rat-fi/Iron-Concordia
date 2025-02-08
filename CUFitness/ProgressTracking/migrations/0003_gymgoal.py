# Generated by Django 5.1.5 on 2025-02-08 18:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ProgressTracking", "0002_dailyfitnessgoal"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GymGoal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cardio", models.FloatField(default=0)),
                ("weight_lifting", models.FloatField(default=0)),
                ("yoga", models.FloatField(default=0)),
                ("pilates", models.FloatField(default=0)),
                ("hiit", models.FloatField(default=0)),
                ("cycling", models.FloatField(default=0)),
                ("swimming", models.FloatField(default=0)),
                ("running", models.FloatField(default=0)),
                ("rowing", models.FloatField(default=0)),
                ("boxing", models.FloatField(default=0)),
                ("dancing", models.FloatField(default=0)),
                ("strength_training", models.FloatField(default=0)),
                ("crossfit", models.FloatField(default=0)),
                ("stretching", models.FloatField(default=0)),
                ("elliptical_trainer", models.FloatField(default=0)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
