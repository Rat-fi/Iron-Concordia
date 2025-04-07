from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
import datetime, calendar
from django.contrib.auth.decorators import login_required
from .models import DailyFitnessGoal, Question, GymGoal, ExerciseSession, exercises
from .models import Badge, UserBadge, Award, UserAward
from django.db.models import Sum, Max
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

        new_session = ExerciseSession.objects.create(
            user=request.user,
            exercise_type=exercise_type,
            exercise_time=duration
        )
        context['message'] = "Your exercise session has been recorded."

        streak_day = 5
        today = datetime.date.today()
        dates = [today - datetime.timedelta(days=i) for i in range(streak_day)]
        sessions_dates = ExerciseSession.objects.filter(
            user = request.user,
            recorded_at__date__in=dates
        ).values_list('recorded_at__date', flat=True).distinct()
        if len(set(sessions_dates)) == streak_day:
            if not UserBadge.objects.filter(user=request.user, badge__name="5 Day Streak").exists():
                badge, created = Badge.objects.get_or_create(
                    name = "5 Day Streak",
                    defaults = {'description': 'Congratulations! You have exercised 5 days in a row.'}
                )
                UserBadge.objects.create(user=request.user, badge=badge)
                context['badge_message'] = "Congratulations! You have earned the 5 Day Streak badge."

        if new_session.recorded_at.time() < datetime.time(7, 0):
            if not UserBadge.objects.filter(user=request.user, badge__name="Early Bird").exists():
                badge, created = Badge.objects.get_or_create(
                    name="Early Bird",
                    defaults={'description': 'Great job getting your workout in early before 7 AM!'}
                )
                UserBadge.objects.create(user=request.user, badge=badge)
                context['badge_message'] = context.get('badge_message', '') + " You've earned the 'Early Bird' badge!"

        cumulative_days = ExerciseSession.objects.filter(user=request.user) \
            .values_list('recorded_at__date', flat=True).distinct().count()

        step = 50
        cumulative_thresholds = list(range(step, cumulative_days + 1, step))

        for threshold in cumulative_thresholds:
            badge_name = f"{threshold} Day Milestone"
            if not UserBadge.objects.filter(user=request.user, badge__name=badge_name).exists():
                badge, created = Badge.objects.get_or_create(
                    name=badge_name,
                    defaults={'description': f"Congratulations! You have exercised on {threshold} different days."}
                )
                UserBadge.objects.create(user=request.user, badge=badge)
                context['badge_message'] = context.get('badge_message', '') + f" You've earned the '{badge_name}' badge!"


        if exercise_type == 'elliptical_trainer':
            elliptical_count = ExerciseSession.objects.filter(user=request.user, exercise_type= 'elliptical_trainer').count()
            if elliptical_count == 1:
                award, created = Award.objects.get_or_create(
                    name="My First Elliptical Workout",
                    defaults={'description': 'Great job on completing your first elliptical workout!'}
                )
                if not UserAward.objects.filter(user=request.user, award=award).exists():
                    UserAward.objects.create(user=request.user, award=award)
                    context['award_message'] = "You've earned the 'My First Elliptical Workout' award!"

        prev_best = ExerciseSession.objects.filter(
            user=request.user, 
            exercise_type=exercise_type
        ).exclude(id=new_session.id).aggregate(max_time=Max('exercise_time'))['max_time']
        if prev_best is None or duration > prev_best:
            
            exercise_dict = dict(exercises)
            award_name = f"New Move Record for {exercise_dict.get(exercise_type, exercise_type)}"
            award, created = Award.objects.get_or_create(
                name=award_name,
                defaults={'description': f"Congratulations on setting a new record for {exercise_dict.get(exercise_type, exercise_type)}!"}
            )
            if not UserAward.objects.filter(user=request.user, award=award).exists():
                UserAward.objects.create(user=request.user, award=award)
                if 'award_message' in context:
                    context['award_message'] += f" Also, you've earned the '{award_name}' award!"
                else:
                    context['award_message'] = f"You've earned the '{award_name}' award!"

    return render(request, 'progressTracking/trackExercise.html', context)

@login_required
def my_awards(request):

    user_badges = UserBadge.objects.filter(user=request.user)
    user_awards = UserAward.objects.filter(user=request.user)
    context = {
         'badges': user_badges,
         'awards': user_awards,
    }
    return render(request, 'progressTracking/awards.html', context)


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