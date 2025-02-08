from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
import datetime, calendar
from django.contrib.auth.decorators import login_required
from .models import DailyFitnessGoal, Question, GymGoal, ExerciseSession, exercises
from django.db.models import Sum



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




@login_required
def daily_summary(request):
    today = datetime.date.today()
    # Aggregate today's sessions: convert exercise_time (seconds) into minutes.
    daily_records = (
        ExerciseSession.objects
        .filter(user=request.user, recorded_at__date=today)
        .values('exercise_type')
        .annotate(total_time=Sum('exercise_time'))
    )
    
    # Build a dictionary mapping exercise_type to total minutes.
    daily_summary_dict = {}
    for rec in daily_records:
        exercise_type = rec['exercise_type']
        total_seconds = rec['total_time'] or 0
        daily_summary_dict[exercise_type] = total_seconds / 60.0  # Convert seconds to minutes

    # Fetch the user's gym goals.
    try:
        gym_goal = GymGoal.objects.get(user=request.user)
    except GymGoal.DoesNotExist:
        gym_goal = None

    # Define the exercise fields (field name, display name).
    exercise_fields = [
        ('cardio', 'Cardio'),
        ('weight_lifting', 'Weight Lifting'),
        ('yoga', 'Yoga'),
        ('pilates', 'Pilates'),
        ('hiit', 'HIIT'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('running', 'Running'),
        ('rowing', 'Rowing'),
        ('boxing', 'Boxing'),
        ('dancing', 'Dancing'),
        ('strength_training', 'Strength Training'),
        ('crossfit', 'CrossFit'),
        ('stretching', 'Stretching'),
        ('elliptical_trainer', 'Elliptical Trainer'),
    ]
    
    summary_list = []
    if gym_goal:
        for key, label in exercise_fields:
            # Weekly goal is stored in hours.
            weekly_goal = getattr(gym_goal, key)
            # Compute daily goal in minutes.
            daily_goal = (weekly_goal / 7) * 60
            daily_progress = daily_summary_dict.get(key, 0)
            difference = daily_goal - daily_progress
            summary_list.append({
                'exercise_key': key,
                'exercise_label': label,
                'daily_progress': daily_progress,
                'daily_goal': daily_goal,
                'difference': difference,
            })
    
    context = {
        'today': today,
        'summary_list': summary_list,
    }
    return render(request, 'progressTracking/dailySummary.html', context)



@login_required
def weekly_summary(request):
    today = datetime.date.today()
    # Compute the start (Monday) and end (Sunday) of the current week.
    start_week = today - datetime.timedelta(days=today.weekday())
    end_week = start_week + datetime.timedelta(days=6)
    
    # Aggregate the weekly exercise sessions (summing exercise_time in seconds).
    weekly_records = (
        ExerciseSession.objects
        .filter(user=request.user, recorded_at__date__gte=start_week, recorded_at__date__lte=end_week)
        .values('exercise_type')
        .annotate(total_time=Sum('exercise_time'))
    )
    
    # Convert aggregated seconds into hours.
    weekly_summary_dict = {}
    for rec in weekly_records:
        exercise_type = rec['exercise_type']
        total_seconds = rec['total_time'] or 0
        weekly_summary_dict[exercise_type] = total_seconds / 3600.0  # hours

    # Get the user's weekly gym goals.
    try:
        gym_goal = GymGoal.objects.get(user=request.user)
    except GymGoal.DoesNotExist:
        gym_goal = None

    # List of exercise fields (field name, display name).
    exercise_fields = [
        ('cardio', 'Cardio'),
        ('weight_lifting', 'Weight Lifting'),
        ('yoga', 'Yoga'),
        ('pilates', 'Pilates'),
        ('hiit', 'HIIT'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('running', 'Running'),
        ('rowing', 'Rowing'),
        ('boxing', 'Boxing'),
        ('dancing', 'Dancing'),
        ('strength_training', 'Strength Training'),
        ('crossfit', 'CrossFit'),
        ('stretching', 'Stretching'),
        ('elliptical_trainer', 'Elliptical Trainer'),
    ]
    
    summary_list = []
    if gym_goal:
        for key, label in exercise_fields:
            weekly_goal = getattr(gym_goal, key)
            weekly_progress = weekly_summary_dict.get(key, 0)
            difference = weekly_goal - weekly_progress
            summary_list.append({
                'exercise_key': key,
                'exercise_label': label,
                'weekly_progress': weekly_progress,
                'weekly_goal': weekly_goal,
                'difference': difference,
            })
    else:
        # If the user has no GymGoal set, still show progress.
        for key, label in exercise_fields:
            weekly_progress = weekly_summary_dict.get(key, 0)
            summary_list.append({
                'exercise_key': key,
                'exercise_label': label,
                'weekly_progress': weekly_progress,
                'weekly_goal': 0,
                'difference': 0 - weekly_progress,
            })
    
    context = {
        'start_week': start_week,
        'end_week': end_week,
        'summary_list': summary_list,
    }
    return render(request, 'progressTracking/weeklySummary.html', context)


@login_required
def monthly_summary(request):
    today = datetime.date.today()
    first_day = datetime.date(today.year, today.month, 1)
    last_day = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    
    # Aggregate the monthly exercise sessions.
    monthly_records = (
        ExerciseSession.objects
        .filter(user=request.user, recorded_at__date__gte=first_day, recorded_at__date__lte=last_day)
        .values('exercise_type')
        .annotate(total_time=Sum('exercise_time'))
    )
    
    monthly_summary_dict = {}
    for rec in monthly_records:
        exercise_type = rec['exercise_type']
        total_seconds = rec['total_time'] or 0
        monthly_summary_dict[exercise_type] = total_seconds / 3600.0  # hours

    try:
        gym_goal = GymGoal.objects.get(user=request.user)
    except GymGoal.DoesNotExist:
        gym_goal = None

    # Use the same exercise fields list.
    exercise_fields = [
        ('cardio', 'Cardio'),
        ('weight_lifting', 'Weight Lifting'),
        ('yoga', 'Yoga'),
        ('pilates', 'Pilates'),
        ('hiit', 'HIIT'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('running', 'Running'),
        ('rowing', 'Rowing'),
        ('boxing', 'Boxing'),
        ('dancing', 'Dancing'),
        ('strength_training', 'Strength Training'),
        ('crossfit', 'CrossFit'),
        ('stretching', 'Stretching'),
        ('elliptical_trainer', 'Elliptical Trainer'),
    ]
    
    summary_list = []
    if gym_goal:
        # For monthly summary, we assume a monthly goal is roughly 4 times the weekly goal.
        for key, label in exercise_fields:
            weekly_goal = getattr(gym_goal, key)
            monthly_goal = weekly_goal * 4
            monthly_progress = monthly_summary_dict.get(key, 0)
            difference = monthly_goal - monthly_progress
            summary_list.append({
                'exercise_key': key,
                'exercise_label': label,
                'monthly_progress': monthly_progress,
                'monthly_goal': monthly_goal,
                'difference': difference,
            })
    else:
        for key, label in exercise_fields:
            monthly_progress = monthly_summary_dict.get(key, 0)
            summary_list.append({
                'exercise_key': key,
                'exercise_label': label,
                'monthly_progress': monthly_progress,
                'monthly_goal': 0,
                'difference': 0 - monthly_progress,
            })
    
    context = {
        'first_day': first_day,
        'last_day': last_day,
        'summary_list': summary_list,
    }
    return render(request, 'progressTracking/monthlySummary.html', context)










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