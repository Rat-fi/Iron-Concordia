import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..forms.PersonalizedPlan import UserInfoForm
from ..models.PersonalizedPlan import  FitnessPlan

@login_required
def collect_user_info_view(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            
            payload = {
                "age": user_data['age'],
                "weight": user_data['weight'],
                "height": user_data['height'],
                "fitness_goal": user_data['goal'],
                "gender": user_data['gender'],
                "dietary_restrictions": user_data['dietary_restrictions'],
            }
            
            try:
                ai_url = "http://127.0.0.1:8000/Agent/generate_plan/"
                cookies = {
                    'csrftoken': request.COOKIES.get('csrftoken', ''),
                    'sessionid': request.COOKIES.get('sessionid', ''),
                }
                headers = {
                    "Content-Type": "application/json",
                    "X-CSRFToken": cookies['csrftoken'],
                    }
                response = requests.post(ai_url, data=json.dumps(payload), headers=headers, cookies=cookies, timeout=15)

                if response.status_code == 200:
                    data = response.json()
                    ai_plan = data.get('response', 'No Plan Found')

                    fitness_plan, created = FitnessPlan.objects.update_or_create(
                        user=request.user,
                        defaults={'plan_content': ai_plan}
                    )
                    return redirect('view_plan')
                else:
                    form.add_error(None, f"Failed to get AI Plan, Error: {response.status_code}")
            except requests.RequestException as e:
                form.add_error(None, f"Failed to get AI Plan, {str(e)}")

        
        
    else:
        form = UserInfoForm()

    return render(request, 'fitnessplan/collect_user_info.html', {'form': form})
    

@login_required
def view_plan_view(request):
    try:
        fitness_plan = FitnessPlan.objects.get(user=request.user)
    except FitnessPlan.DoesNotExist:
        fitness_plan = None

    return render(request, 'fitnessplan/view_plan.html', {'fitness_plan': fitness_plan})


@login_required
def adjust_plan_view(request):
    fitness_plan = get_object_or_404(FitnessPlan, user=request.user)

    if request.method == 'POST':
        new_content = request.POST.get('plan_content')
        fitness_plan.plan_content = new_content
        fitness_plan.save()
        return redirect('view_plan')
    
    return render(request, 'fitnessplan/adjust_plan.html', {'fitness_plan': fitness_plan})
