from django.shortcuts import render
from ..models.Budget import BudgetMeal
from ..forms.BudgetForm import BudgetForm

def budget_meallist(request):
    meals = BudgetMeal.objects.all()
    budget = None

    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.cleaned_data['budget']
            meals = meals.filter(price__lte=budget)
    else:
        form = BudgetForm()

    return render(request, 'mealplan/budget_meallist.html', {'form':form, 'meals':meals})