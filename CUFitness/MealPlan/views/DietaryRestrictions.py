from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..forms.DietaryRestrictionsForm import DietaryRestrictionsMealPlanForm, DietaryRestrictionsForm
from ..models.DietaryRestrictions import DietaryRestrictions_MealPlan, DietaryRestrictions

@login_required
def create_meal_plan(request):
    if request.method == 'POST':
        form = DietaryRestrictionsMealPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meal_plan_list')
    else:
        form = DietaryRestrictionsMealPlanForm()
    return render(request, 'mealplan/create_meal_plan.html', {'form': form})


@login_required
def set_dietary_restrictions(request):
    try:
        restriction = DietaryRestrictions.objects.get(user=request.user)
    except DietaryRestrictions.DoesNotExist:
        restriction = DietaryRestrictions(user=request.user)

    if request.method == 'POST':
        form = DietaryRestrictionsForm(request.POST, instance=restriction)
        if form.is_valid():
            restriction = form.save(commit=False)
            restriction.user = request.user
            restriction.save()
            form.save_m2m()
            return redirect('dashboard')
    else:
        form = DietaryRestrictionsForm(instance=restriction)

    return render(request, 'mealplan/set_dietary_restrictions.html', {'form': form})
