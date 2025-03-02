from django.shortcuts import render
from ..models.BrowseWorkout import BrowseWorkout, Category
from django.db.models import Case, When, IntegerField

def browse_category_list(request):
    categories = Category.objects.all()
    return render(request, 'fitnessplan/browse_category_list.html', {'categories': categories})

def browse_exercise_list(request):
    selected_categories = request.GET.getlist('categories')
    exercises = BrowseWorkout.objects.all()

    if selected_categories:
        exercises = exercises.filter(category__id__in = selected_categories)

    exercises = exercises.annotate(
    intensity_order=Case(
        When(intensity_level='Low', then=0),
        When(intensity_level='Medium', then=1),
        When(intensity_level='High', then=2),
        default=3,
        output_field=IntegerField()
    )
).order_by('name', 'duration', 'intensity_order')

    return render(request, 'fitnessplan/browse_exercise_list.html', {'exercises': exercises})
