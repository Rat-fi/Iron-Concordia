from django.core.paginator import Paginator
from django.shortcuts import render
from MealPlan.models import MealplanSearchbar

def MealPlan_Searchbar(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    MealPlan_Sbresult = MealplanSearchbar.objects.all() #get all the data of MealPlan from the database 

    if query:
        MealPlan_Sbresult = MealPlan_Sbresult.filter(name__icontains=query)
    if category:
        MealPlan_Sbresult = MealPlan_Sbresult.filter(category=category)

    MealPlan_Sbresult = MealPlan_Sbresult.order_by('id')

    paginator = Paginator(MealPlan_Sbresult, 10) 
    page_number = request.GET.get('page')   
    page_obj = paginator.get_page(page_number)  

    return render(request, 'mealplan/MealPlan_Searchbar.html', {'page_obj': page_obj, 'query': query, 'category': category})
