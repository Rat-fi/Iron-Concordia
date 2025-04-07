from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models.AddWorkout import WorkoutPlan
from ..forms.AddWorkout import WorkoutForm

def create_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save()
            messages.success(request, f"Workout Plan {workout.workout_name} is saved successfully!")
            return redirect('workout-detail', pk=workout.pk)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = WorkoutForm()
    return render(request, 'fitnessplan/AddWorkout.html', {'form': form})

def workout_detail(request,pk):
    workout = get_object_or_404(WorkoutPlan, pk=pk)
    return render(request, 'fitnessplan/WorkoutDetail.html', {'workout': workout})

def workout_list(request):
    workouts = WorkoutPlan.objects.all().order_by('-created_at')
    return render(request, 'fitnessplan/WorkoutList.html', {'workouts': workouts})

def workout_edit(request, pk):
    workout = get_object_or_404(WorkoutPlan, id=pk)

    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            workout = form.save()
            messages.success(request, "Workout updated successfully.")
            return redirect('workout-detail', pk=workout.id)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = WorkoutForm(instance=workout)

    return render(request, 'fitnessplan/edit_workout.html', {
        'form': form,
        'workout': workout
    })


