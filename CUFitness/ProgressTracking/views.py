from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
import datetime, calendar
from django.contrib.auth.decorators import login_required
from .models import DailyFitnessGoal, Question, GymGoal, ExerciseSession, exercises
from django.db.models import Sum
import json



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

    try:
        gym_goal = GymGoal.objects.get(user=request.user)
    except GymGoal.DoesNotExist:
        gym_goal = GymGoal(user=request.user)

    goal_values = {}
    for field, _ in exercises:
        goal_values[field] = getattr(gym_goal, field, 0)
    context['goal_values'] = goal_values

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        error = None
        for field, _ in exercises:
            try:
                value = float(request.POST.get(field, 0) or 0)
            except ValueError:
                error = "Please enter valid numeric values for all fields."
                break
            setattr(gym_goal, field, value)
        if error:
            context['error'] = error
        else:
            gym_goal.goal_date = datetime.date.today()
            gym_goal.save()
            context['message'] = "Your gym goals have been updated."
            for field, _ in exercises:
                goal_values[field] = getattr(gym_goal, field, 0)
            context['goal_values'] = goal_values
    context['gym_goal'] = gym_goal  
    return render(request, 'progressTracking/setMyGymGoals.html', context)

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
    if record.recorded_at.date() != today:
        return redirect('today_exercise_records')
    
    if request.method == 'POST':
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
    
    daily_records = (
        ExerciseSession.objects
        .filter(user=request.user, recorded_at__date=today)
        .values('exercise_type')
        .annotate(total_time=Sum('exercise_time'))
    )
    
    daily_summary_dict = {}
    for rec in daily_records:
        exercise_type = rec['exercise_type']
        total_seconds = rec['total_time'] or 0
        daily_summary_dict[exercise_type] = total_seconds / 60.0  # minutes
    
    try:
        gym_goal = GymGoal.objects.get(user=request.user)
    except GymGoal.DoesNotExist:
        gym_goal = None

    if gym_goal:
        start_week = today - datetime.timedelta(days=today.weekday())
        end_week = start_week + datetime.timedelta(days=6)
        if not (start_week <= gym_goal.updated.date() <= end_week):
            gym_goal = None  

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
    for key, label in exercise_fields:
        daily_progress = daily_summary_dict.get(key, 0)
        if gym_goal:
            weekly_goal = getattr(gym_goal, key)
            daily_goal = (weekly_goal / 7) * 60
        else:
            daily_goal = 0
        difference = daily_goal - daily_progress
        
        if daily_progress > 0 or daily_goal > 0:
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
    start_week = today - datetime.timedelta(days=today.weekday())
    end_week = start_week + datetime.timedelta(days=6)
    
    weekly_records = (
        ExerciseSession.objects
        .filter(user=request.user, recorded_at__date__gte=start_week, recorded_at__date__lte=end_week)
        .values('exercise_type')
        .annotate(total_time=Sum('exercise_time'))
    )
    
    weekly_summary_dict = {}
    for rec in weekly_records:
        exercise_type = rec['exercise_type']
        total_seconds = rec['total_time'] or 0
        weekly_summary_dict[exercise_type] = total_seconds / 3600.0  # hours

    try:
        gym_goal = GymGoal.objects.get(user=request.user)
    except GymGoal.DoesNotExist:
        gym_goal = None

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

@login_required
def history_activity(request):
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    
    records = ExerciseSession.objects.filter(user=request.user)
    error = None
    today = datetime.date.today()
    start_date = None
    end_date = None
    
    if start_date_str:
        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            error = "Invalid start date format. Use YYYY-MM-DD."
    if end_date_str:
        try:
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            error = "Invalid end date format. Use YYYY-MM-DD."
    
    if start_date and end_date:
        if start_date > end_date:
            error = "Start date cannot be later than end date."
            records = records.none()
        else:
            records = records.filter(recorded_at__date__gte=start_date, recorded_at__date__lte=end_date)
    else:
        if start_date:
            records = records.filter(recorded_at__date__gte=start_date)
        if end_date:
            if end_date > today:
                end_date = today
                end_date_str = today.strftime('%Y-%m-%d')
            records = records.filter(recorded_at__date__lte=end_date)
    
    records_list = []
    for r in records.order_by('-recorded_at'):
        r.exercise_minutes = r.exercise_time / 60.0  # minutes as float
        records_list.append(r)
    
    context = {
        'records': records_list,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'error': error,
        'today': today.strftime('%Y-%m-%d'),
    }
    return render(request, 'progressTracking/historyActivity.html', context)

@login_required
def weekly_activity_chart(request):
    today = datetime.date.today()
    # Determine current week: Monday to Sunday
    start_week = today - datetime.timedelta(days=today.weekday())
    end_week = start_week + datetime.timedelta(days=6)

    # Build list of dates and labels (e.g., Monday, Tuesday, …)
    days = [start_week + datetime.timedelta(days=i) for i in range(7)]
    day_labels = [day.strftime("%A") for day in days]

    # Initialize a dictionary: for each exercise type, a list of 7 zeros.
    exercise_data = {}
    for ex, label in exercises:
        exercise_data[ex] = [0] * 7

    # Query sessions for the current week
    sessions = ExerciseSession.objects.filter(
        user=request.user,
        recorded_at__date__gte=start_week,
        recorded_at__date__lte=end_week
    )

    # Aggregate total time (in minutes) per exercise type for each day.
    # Assume exercise_time is stored in seconds.
    for session in sessions:
        day_index = (session.recorded_at.date() - start_week).days
        # Convert seconds to minutes:
        exercise_data[session.exercise_type][day_index] += session.exercise_time / 60.0

    # Define a mapping for colors for each exercise type.
    color_mapping = {
        'cardio': '#FF6384',
        'weight_lifting': '#36A2EB',
        'yoga': '#FFCE56',
        'pilates': '#4BC0C0',
        'hiit': '#9966FF',
        'cycling': '#FF9F40',
        'swimming': '#66FF66',
        'running': '#FF6666',
        'rowing': '#66FFFF',
        'boxing': '#FF99CC',
        'dancing': '#CCCCFF',
        'strength_training': '#FFCC99',
        'crossfit': '#99FFCC',
        'stretching': '#CCCC99',
        'elliptical_trainer': '#FFCCFF',
    }

    # Prepare Chart.js datasets. Only include an exercise if there is some recorded time.
    datasets = []
    for ex, label in exercises:
        data = exercise_data[ex]
        if any(val > 0 for val in data):
            datasets.append({
                'label': label,
                'data': data,
                'backgroundColor': color_mapping.get(ex, '#000000'),
            })

    chart_data = {
        'labels': day_labels,
        'datasets': datasets,
    }

    context = {
        'chart_data': json.dumps(chart_data),
        'start_week': start_week,
        'end_week': end_week,
    }
    return render(request, 'progressTracking/weeklyActivityChart.html', context)






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