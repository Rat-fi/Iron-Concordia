from django.shortcuts import render, redirect # render is used to render the html file and return an http response, redirect is used to redirect the user to another page
from django.contrib.auth.decorators import login_required
from ..forms.DietaryRestrictionsForm import DietaryRestrictionsForm
from ..models.DietaryRestrictions import DietaryRestrictions,DietaryRestrictions_MealPlan

@login_required
def set_dietary_restrictions(request):
    restrictions, created = DietaryRestrictions.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = DietaryRestrictionsForm(request.POST, instance = restrictions)
        if form.is_valid():
            form.save()
            return redirect('meal_plan')
    else:
        form = DietaryRestrictionsForm(instance = restrictions)
    return render(request, 'DietaryRestrictions/set_dietary_restrictions.html', {'form': form})
    

@login_required
def meal_plan(request):
    restrictions, created = DietaryRestrictions.objects.get_or_create(user=request.user)

    meals = DietaryRestrictions_MealPlan.objects.all()
    if restrictions.is_vegetarian:
        meals = meals.filter(is_vegetarian=True)
    if restrictions.is_vegan:
        meals = meals.filter(is_vegan=True)
    if restrictions.is_gluten_Free:
        meals = meals.exclude(contains_gluten=True)
    if restrictions.is_lactose_Free:
        meals = meals.exclude(contains_lactose=True)
    if restrictions.is_nut_Free:
        meals = meals.exclude(contains_nuts=True)
    if restrictions.is_shellfish_Free:
        meals = meals.exclude(contains_shellfish=True)
    if restrictions.is_soy_free:
        meals = meals.exclude(contains_soy=True)
    if restrictions.is_egg_free:
        meals = meals.exclude(contains_eggs=True)
    if restrictions.is_pork_free:
        meals = meals.exclude(contains_pork=True)
    if restrictions.is_beef_free:
        meals = meals.exclude(contains_beef=True)
    if restrictions.is_fish_free:
        meals = meals.exclude(contains_fish=True)
    if restrictions.is_poultry_free:
        meals = meals.exclude(contains_poultry=True)

    return render(request, 'DietaryRestrictions/meal_plan.html', {
        'restrictions': restrictions,
        'meals': meals
    })