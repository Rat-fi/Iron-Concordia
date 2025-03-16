from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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

@login_required
def toggle_favorite(request, exercise_id):
    exercise = get_object_or_404(BrowseWorkout, id=exercise_id)
    user = request.user

    if user in exercise.favorited_by.all():
        exercise.favorited_by.remove(user)
    else:
        exercise.favorited_by.add(user)

    return redirect(request.META.get('HTTP_REFERER', 'browse_exercise_list'))


@login_required
def favorite_list(request):
    favorites = request.user.favorite_exercises.all()
    return render(request,'fitnessplan/favorite_list.html', {'favorites': favorites})