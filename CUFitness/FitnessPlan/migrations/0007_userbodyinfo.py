# Generated by Django 5.1.5 on 2025-04-07 17:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitnessPlan', '0006_fitnessplan'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBodyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.PositiveIntegerField()),
                ('weight', models.PositiveIntegerField()),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('fitness_goal', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='body_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
