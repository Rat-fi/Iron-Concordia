from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models.BrowseWorkout import BrowseWorkout, Category
from django.db.models import Case, When, IntegerField

def browse_exercise_list(request):
    selected_categories = request.GET.getlist('categories')
    favorites_only = request.GET.get('favorites_only') == '1'
    categories = Category.objects.all()

    exercises = BrowseWorkout.objects.all()

    if selected_categories:
        exercises = exercises.filter(category__id__in=selected_categories)

    if favorites_only and request.user.is_authenticated:
        exercises = exercises.filter(favorited_by=request.user)

    # Optional sorting logic
    exercises = exercises.annotate(
        intensity_order=Case(
            When(intensity_level='Low', then=0),
            When(intensity_level='Medium', then=1),
            When(intensity_level='High', then=2),
            default=3,
            output_field=IntegerField()
        )
    ).order_by('name', 'duration', 'intensity_order')

    return render(request, 'fitnessplan/exercise_explorer.html', {
        'exercises': exercises,
        'categories': categories,
        'selected_categories': selected_categories,
        'favorites_only': favorites_only,
    })

@login_required
def toggle_favorite(request, exercise_id):
    exercise = get_object_or_404(BrowseWorkout, id=exercise_id)
    user = request.user

    if user in exercise.favorited_by.all():
        exercise.favorited_by.remove(user)
    else:
        exercise.favorited_by.add(user)

    return redirect(request.META.get('HTTP_REFERER', 'browse_exercise_list'))