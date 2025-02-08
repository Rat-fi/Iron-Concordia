# Generated by Django 5.1.5 on 2025-02-08 19:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ProgressTracking", "0003_gymgoal"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ExerciseSession",
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
                (
                    "exercise_type",
                    models.CharField(
                        choices=[
                            ("cardio", "Cardio"),
                            ("weight_lifting", "Weight Lifting"),
                            ("yoga", "Yoga"),
                            ("pilates", "Pilates"),
                            ("hiit", "HIIT"),
                            ("cycling", "Cycling"),
                            ("swimming", "Swimming"),
                            ("running", "Running"),
                            ("rowing", "Rowing"),
                            ("boxing", "Boxing"),
                            ("dancing", "Dancing"),
                            ("strength_training", "Strength Training"),
                            ("crossfit", "CrossFit"),
                            ("stretching", "Stretching"),
                            ("elliptical_trainer", "Elliptical Trainer"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "exercise_time",
                    models.PositiveIntegerField(
                        help_text="Exercise duration in seconds"
                    ),
                ),
                ("recorded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
