from django.contrib import admin
from .models import Question, DailyFitnessGoal

# Register your models here.
admin.site.register(Question)
admin.site.register(DailyFitnessGoal)
