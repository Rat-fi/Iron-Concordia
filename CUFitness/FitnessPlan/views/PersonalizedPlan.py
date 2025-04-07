import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..forms.PersonalizedPlan import UserInfoForm
from ..models.PersonalizedPlan import  FitnessPlan

@login_required
def collect_user_info_view(request):
    user = request.user
    try:
        existing_info = user.body_info  # from OneToOneField relation
    except:
        existing_info = None

    if request.method == 'POST':
        # Distinguish between save and generate
        generate = 'generate_plan' in request.POST

        form = UserInfoForm(request.POST, instance=existing_info)
        if form.is_valid():
            user_info = form.save(commit=False)
            user_info.user = user
            user_info.save()

            if generate:
                payload = {
                    "age": user_info.age,
                    "weight": user_info.weight,
                    "height": user_info.height,
                    "fitness_goal": user_info.fitness_goal,
                    "gender": user_info.gender
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

                        FitnessPlan.objects.update_or_create(
                            user=user,
                            defaults={'plan_content': ai_plan}
                        )
                        return redirect('view_plan')
                    else:
                        form.add_error(None, f"Failed to get AI Plan (Error {response.status_code})")
                except requests.RequestException as e:
                    form.add_error(None, f"AI request failed: {str(e)}")
            else:
                # If just saving user info without generating plan
                return redirect('collect_user_info')

    else:
        form = UserInfoForm(instance=existing_info)

    return render(request, 'fitnessplan/collect_user_info.html', {
        'form': form,
        'current_info': existing_info
    })

    

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
