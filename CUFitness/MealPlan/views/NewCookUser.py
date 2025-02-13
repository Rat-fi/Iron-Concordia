from django.shortcuts import render
from ..models.NewCookUser import MealInstructions

def meal_instructions_list(request):
    instructions = MealInstructions.objects.all()
    
   
    dietary = request.GET.get('dietary_restrictions')
    if dietary:
        instructions = instructions.filter(dietary_restrictions__icontains=dietary)
    
    price_min = request.GET.get('price_min')
    if price_min:
        instructions = instructions.filter(price__gte=price_min)
    price_max = request.GET.get('price_max')
    if price_max:
        instructions = instructions.filter(price__lte=price_max)
    
    prepare_time_max = request.GET.get('prepare_time_max')
    if prepare_time_max:
        instructions = instructions.filter(prepare_time__lte=prepare_time_max)
    
    calories_max = request.GET.get('calories_max')
    if calories_max:
        instructions = instructions.filter(calories__lte=calories_max)
    
    protein_min = request.GET.get('protein_min')
    if protein_min:
        instructions = instructions.filter(protein__gte=protein_min)
    
    context = {
        'instructions': instructions,
    }
    
    return render(request, 'mealplan/newcookuser_list.html', context)