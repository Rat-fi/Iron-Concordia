from django.contrib import admin
from django.urls import path, include
from CUFitness.views import home  # Import home view from CUFitness

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('user/', include('User.urls')),
    path('progressTracking/', include('ProgressTracking.urls')), #TBD
    path('MealPlan/', include('MealPlan.urls')), 
    path('FitnessPlan/', include('FitnessPlan.urls')),
]

