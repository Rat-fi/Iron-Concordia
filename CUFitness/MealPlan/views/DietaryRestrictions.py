from django.shortcuts import render, redirect # render is used to render the html file and return an http response, redirect is used to redirect the user to another page
from django.contrib.auth.decorators import login_required
from ..forms.DietaryRestrictionsForm import DietaryRestrictionsForm
from ..models.DietaryRestrictions import DietaryRestrictions

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

    return render(request, 'DietaryRestrictions/meal_plan.html', {'restrictions': restrictions})