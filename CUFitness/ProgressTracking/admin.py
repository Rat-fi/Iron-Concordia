from django.contrib import admin
from .models import Question, DailyFitnessGoal, Badge, Award, UserBadge, UserAward

# Register your models here.
admin.site.register(Question)
admin.site.register(DailyFitnessGoal)

admin.site.register(Badge)
admin.site.register(Award)
admin.site.register(UserBadge)
admin.site.register(UserAward)
