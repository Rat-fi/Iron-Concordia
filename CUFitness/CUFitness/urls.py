from django.contrib import admin
from django.urls import path, include
from CUFitness.views import home  # Import home view from CUFitness
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('user/', include('User.urls')),
    path('progressTracking/', include('ProgressTracking.urls')), #TBD
    path('MealPlan/', include('MealPlan.urls')), 
    path('FitnessPlan/', include('FitnessPlan.urls')),
    path('Agent/', include('LLMAgent.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

