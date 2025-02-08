from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
import datetime
from django.contrib.auth.decorators import login_required
from .models import DailyFitnessGoal, Question, GymGoal, ExerciseSession, exercises



# Create your views here.
def index(request):
    # username = request.POST["username"]
    # password = request.POST["password"]
    # user = authenticate(request, username=username, password=password)
    latest_question_list = Question.objects.order_by("question_text")[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    output = "index"
    return HttpResponse(output)


@login_required
def set_daily_fitness_goal(request):
    context = {'user': request.user}

    #try to fetch data from the databse first to show 
    try:
        current_goal = DailyFitnessGoal.objects.get(user=request.user)
        context.update({
            'standing_time': current_goal.standing_time,
            'exercise_minutes': current_goal.exercise_minutes,
            'walking_distance': current_goal.walking_distance,
        })
    except DailyFitnessGoal.DoesNotExist:
        pass

    if request.method == 'POST':
        try: 
            standing_time = float(request.POST.get('standing_time') or 0 )
            exercise_minutes = float(request.POST.get('exercise_minutes') or 0 )
            walking_distance = float(request.POST.get('walking_distance') or 0 )
        except ValueError:
            context['error'] = "Please enter valid numeric values."
            return render(request, 'progfressTracking/setFitnessGoal.html', context)

        goal, created = DailyFitnessGoal.objects.update_or_create(
            user=request.user,
            defaults={
                'standing_time': standing_time,
                'exercise_minutes': exercise_minutes,
                'walking_distance': walking_distance,
            }
        )

        context.update({
            'standing_time': standing_time,
            'exercise_minutes': exercise_minutes,
            'walking_distance': walking_distance,
        })

    return render(request, 'progressTracking/setFitnessGoal.html', context)




@login_required
def set_my_gym_goal(request):
    context = {'user': request.user}

    context['exercises'] = exercises

    goals = {}

    try:
        gym_goal = GymGoal.objects.get(user=request.user)
    except GymGoal.DoesNotExist:
        gym_goal = GymGoal(user=request.user)

    if request.method == 'GET':
        for field, _ in exercises:
            goals[field] = getattr(gym_goal, field, 0)
    elif request.method == 'POST':
        error = None
        for field, _ in exercises:
            try:
                # Use 0 as a default if the input is empty.
                value = float(request.POST.get(field, 0) or 0)
            except ValueError:
                error = "Please enter valid numbers for all fields."
                break
            setattr(gym_goal, field, value)
            goals[field] = value
        if error:
            context['error'] = error
        else:
            gym_goal.save()
            context['message'] = "Your gym goals have been updated."

    context['goals'] = goals
    return render(request, 'progressTracking/setMyGymGoal.html', context)

@login_required
def track_exercise(request):
    context = {
        'user': request.user,
        'exercise_choices': exercises,
    }
    
    if request.method == 'POST':
        exercise_type = request.POST.get('exercise_type')
        try:
            duration = int(request.POST.get('duration', 0))
        except ValueError:
            duration = 0

        # Create a new ExerciseSession record
        ExerciseSession.objects.create(
            user=request.user,
            exercise_type=exercise_type,
            exercise_time=duration
        )
        context['message'] = "Your exercise session has been recorded."
    
    return render(request, 'progressTracking/trackExercise.html', context)


@login_required
def today_exercise_records(request):
    today = datetime.date.today()
    records = ExerciseSession.objects.filter(user=request.user, recorded_at__date=today)
    context = {
        'records': records,
        'today': today,
    }
    return render(request, 'progressTracking/todayExerciseRecords.html', context)

@login_required
def edit_exercise_record(request, record_id):
    record = get_object_or_404(ExerciseSession, id=record_id, user=request.user)
    today = datetime.date.today()
    # Restrict editing to only today’s records.
    if record.recorded_at.date() != today:
        return redirect('today_exercise_records')
    
    if request.method == 'POST':
        # Get new values from the submitted form.
        exercise_type = request.POST.get('exercise_type')
        try:
            exercise_time = int(request.POST.get('exercise_time', 0))
        except ValueError:
            exercise_time = record.exercise_time
        record.exercise_type = exercise_type
        record.exercise_time = exercise_time
        record.save()
        return redirect('today_exercise_records')
    else:
        context = {
            'record': record,
            'exercise_choices': exercises,
        }
        return render(request, 'progressTracking/editExerciseRecord.html', context)

@login_required
def remove_exercise_record(request, record_id):
    record = get_object_or_404(ExerciseSession, id=record_id, user=request.user)
    
    if request.method == 'POST':
        record.delete()
        return redirect('today_exercise_records')
    
    return redirect('today_exercise_records')




def checkHistoryData(request, id):
    return HttpResponse(f"history data")
    

def result(request, question_id):
    response = "This is a testing function %s."
    return HttpResponse(response % question_id)

def detail(request, question_id):
    response = "You're looking at question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    response = "You're voting on question %s."
    return HttpResponse(response % question_id)