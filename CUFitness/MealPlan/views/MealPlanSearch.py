from django.shortcuts import render
from ..models.DietaryRestrictions import DietaryRestrictions_MealPlan
from django.db.models import Q

def search_meal_plans(request):
    query = request.GET.get('q', '')
    difficulty = request.GET.get('difficulty', '')
    cal_min = request.GET.get('cal_min')
    cal_max = request.GET.get('cal_max')
    protein_min = request.GET.get('protein_min')
    protein_max = request.GET.get('protein_max')

    # Dietary restriction filters: exclude meals containing these
    dietary_fields = [
        'contains_gluten', 'contains_lactose', 'contains_nuts', 'contains_shellfish',
        'contains_soy', 'contains_eggs', 'contains_pork', 'contains_beef',
        'contains_fish', 'contains_poultry'
    ]
    dietary_filters = {field: request.GET.get(field) == 'on' for field in dietary_fields}

    # Vegetarian/vegan inclusion filters
    is_vegetarian = request.GET.get('is_vegetarian') == 'on'
    is_vegan = request.GET.get('is_vegan') == 'on'

    meal_plans = DietaryRestrictions_MealPlan.objects.all()

    if query:
        meal_plans = meal_plans.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if difficulty:
        meal_plans = meal_plans.filter(difficulty=difficulty)

    if cal_min:
        meal_plans = meal_plans.filter(calories__gte=cal_min)
    if cal_max:
        meal_plans = meal_plans.filter(calories__lte=cal_max)

    if protein_min:
        meal_plans = meal_plans.filter(protein__gte=protein_min)
    if protein_max:
        meal_plans = meal_plans.filter(protein__lte=protein_max)

    # Exclude items that contain the selected ingredients
    for field, value in dietary_filters.items():
        if value:
            meal_plans = meal_plans.exclude(**{field: True})

    # Include only vegetarian/vegan if selected
    if is_vegetarian:
        meal_plans = meal_plans.filter(is_vegetarian=True)
    if is_vegan:
        meal_plans = meal_plans.filter(is_vegan=True)

    checked_fields = [field for field, checked in {**dietary_filters, 'is_vegetarian': is_vegetarian, 'is_vegan': is_vegan}.items() if checked]

    return render(request, "MealPlan/search_meal_plans.html", {
        "meal_plans": meal_plans,
        "query": query,
        "difficulty": difficulty,
        "cal_min": cal_min,
        "cal_max": cal_max,
        "protein_min": protein_min,
        "protein_max": protein_max,
        "checked_fields": checked_fields,
        "dietary_fields": dietary_fields,
    })
