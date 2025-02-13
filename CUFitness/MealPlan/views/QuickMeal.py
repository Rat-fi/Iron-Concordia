from django.shortcuts import render
from ..models.QuickMeal import QuickMeal

def quick_meal_list(request):
    prep_time = request.GET.get("prep_time")
    meals = QuickMeal.objects.all()

    if prep_time:
        meals = meals.filter(preparation_time__lte=int(prep_time))  # 过滤出准备时间小于等于给定值的短食谱

    return render(request, "mealplan/quickmeal_list.html", {"meals": meals})
