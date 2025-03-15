from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import ChatMessage
from ProgressTracking.models import FitnessActivity
from MealPlan.models.DietaryRestrictions import DietaryRestrictions, DietaryRestrictions_MealPlan
from MealPlan.models.QuickMeal import QuickMeal
from MealPlan.models.NewCookUser import MealInstructions
from MealPlan.models.CampusOptions import CampusOptions_MenuItem, CampusOptions_Restaurant
import google.generativeai as genai
import os
from dotenv import load_dotenv
import traceback
import json

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("No API key found. Set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_available_activities():
    """Get all available activities from the database"""
    activities = FitnessActivity.objects.all().values(
        'exercise_type', 
        'recommended_duration_minutes',
        'calories_per_minute', 
        'difficulty_level',
        'target_category',
        'description'
    )
    
    return list(activities)

def get_user_dietary_restrictions(user_id=None):
    """Get user's dietary restrictions if available"""
    try:
        if user_id:
            restrictions = DietaryRestrictions.objects.filter(user_id=user_id).first()
            if restrictions:
                return {
                    'is_vegetarian': restrictions.is_vegetarian,
                    'is_vegan': restrictions.is_vegan,
                    'is_gluten_free': restrictions.is_gluten_Free,
                    'is_lactose_free': restrictions.is_lactose_Free,
                    'is_nut_free': restrictions.is_nut_Free,
                    'is_shellfish_free': restrictions.is_shellfish_Free,
                    'is_soy_free': restrictions.is_soy_free,
                    'is_egg_free': restrictions.is_egg_free,
                    'is_pork_free': restrictions.is_pork_free,
                    'is_beef_free': restrictions.is_beef_free,
                    'is_fish_free': restrictions.is_fish_free,
                    'is_poultry_free': restrictions.is_poultry_free
                }
    except Exception as e:
        print(f"Error fetching dietary restrictions: {e}")
    
    return None

def get_available_meal_plans():
    """Get all available meal plans from the database"""
    meal_plans = DietaryRestrictions_MealPlan.objects.all().values(
        'id',
        'name',
        'description',
        'calories',
        'protein',
        'is_vegetarian',
        'is_vegan',
        'contains_gluten',
        'contains_lactose',
        'contains_nuts',
        'contains_shellfish',
        'contains_soy',
        'contains_eggs',
        'contains_pork',
        'contains_beef',
        'contains_fish',
        'contains_poultry'
    )
    
    return list(meal_plans)

def get_meal_instructions():
    """Get all available meal instructions from the database"""
    instructions = MealInstructions.objects.all().values(
        'id',
        'name',
        'difficulty',
        'dietary_restrictions',
        'price',
        'prepare_time',
        'calories',
        'protein',
        'steps'
    )
    
    return list(instructions)

def get_quick_meals():
    """Get all available quick meals from the database"""
    quick_meals = QuickMeal.objects.all().values(
        'id',
        'name',
        'preparation_time',
        'cooking_materials'
    )
    
    return list(quick_meals)

def get_restaurant_options():
    """Get all available restaurant options from the database"""
    restaurants = CampusOptions_Restaurant.objects.all().values(
        'id',
        'name',
        'address',
        'rating'
    )
    
    restaurant_data = []
    for restaurant in restaurants:
        menu_items = CampusOptions_MenuItem.objects.filter(restaurant_id=restaurant['id']).values(
            'id',
            'name',
            'category',
            'dietary_restrictions',
            'price'
        )
        restaurant['menu_items'] = list(menu_items)
        restaurant_data.append(restaurant)
    
    return restaurant_data

def generate_fitness_response(conversation_history, user_data=None):
    """Generate a response using Gemini 1.5 Flash with constraints from the database"""
    available_activities = get_available_activities()
    available_meal_plans = get_available_meal_plans()
    meal_instructions = get_meal_instructions()
    quick_meals = get_quick_meals()
    restaurant_options = get_restaurant_options()
    
    activities_text = ""
    for activity in available_activities:
        activities_text += f"- {activity['exercise_type']} ({activity['difficulty_level']}): {activity['description'] or 'No description available'}\n"
    
    meal_plans_text = ""
    for meal in available_meal_plans:
        restrictions = []
        if meal['is_vegetarian']: restrictions.append("vegetarian")
        if meal['is_vegan']: restrictions.append("vegan")
        if meal['contains_gluten']: restrictions.append("contains gluten")
        if meal['contains_lactose']: restrictions.append("contains lactose")
        if meal['contains_nuts']: restrictions.append("contains nuts")
        if meal['contains_shellfish']: restrictions.append("contains shellfish")
        if meal['contains_soy']: restrictions.append("contains soy")
        if meal['contains_eggs']: restrictions.append("contains eggs")
        if meal['contains_pork']: restrictions.append("contains pork")
        if meal['contains_beef']: restrictions.append("contains beef")
        if meal['contains_fish']: restrictions.append("contains fish")
        if meal['contains_poultry']: restrictions.append("contains poultry")
        
        restrictions_str = ", ".join(restrictions) if restrictions else "No specific restrictions"
        meal_plans_text += f"- {meal['name']}: {meal['calories']} calories, {meal['protein']}g protein. Dietary info: {restrictions_str}. {meal['description'] or 'No description available'}\n"
    
    instructions_text = ""
    for instruction in meal_instructions:
        instructions_text += f"- {instruction['name']} (Cook at home - {instruction['difficulty']} difficulty): {instruction['calories']} calories, {instruction['protein']}g protein, prep time: {instruction['prepare_time']} mins, price: ${instruction['price']}. Dietary restrictions: {instruction['dietary_restrictions'] or 'None'}\n"
    
    quick_meals_text = ""
    for meal in quick_meals:
        quick_meals_text += f"- {meal['name']} (Quick meal): Preparation time {meal['preparation_time']} minutes. Requires: {meal['cooking_materials']}\n"
    
    restaurant_text = ""
    for restaurant in restaurant_options:
        restaurant_text += f"- {restaurant['name']} (Rating: {restaurant['rating']})\n"
        for item in restaurant['menu_items']:
            restaurant_text += f"  * {item['name']} ({item['category']}): ${item['price']}, Dietary type: {item['dietary_restrictions']}\n"
    
    prompt = """You are a professional fitness and nutrition coach AI assistant. 
Provide personalized workout plans, nutrition advice, meal recommendations, and fitness guidance.
Be encouraging, specific, and considerate of the user's goals, dietary restrictions, and limitations.

IMPORTANT RULES:
1. You must ONLY recommend exercises and activities from the "Available Exercises" list.
2. You must ONLY recommend meals from the "Available Meal Plans", "Home Cooking Meals", "Quick Meals", or "Restaurant Options" lists.
3. Always respect dietary restrictions when recommending meals.
4. Be specific when referencing meals or exercises - use the exact names from the lists.

Available Exercises:
"""
    
    prompt += activities_text
    
    prompt += "\nAvailable Meal Plans:\n"
    prompt += meal_plans_text
    
    prompt += "\nHome Cooking Meals:\n"
    prompt += instructions_text
    
    prompt += "\nQuick Meals:\n"
    prompt += quick_meals_text
    
    prompt += "\nRestaurant Options:\n"
    prompt += restaurant_text
    
    if user_data:
        dietary_restrictions = None
        if user_data.get('user_id'):
            dietary_restrictions = get_user_dietary_restrictions(user_data.get('user_id'))
        
        prompt += f"""
User information:
- Age: {user_data.get('age', 'Unknown')}
- Weight: {user_data.get('weight', 'Unknown')} {user_data.get('weight_unit', 'kg')}
- Height: {user_data.get('height', 'Unknown')} {user_data.get('height_unit', 'cm')}
- Fitness Goals: {user_data.get('fitness_goals', 'Not specified')}
- Health Restrictions: {user_data.get('health_restrictions', 'None mentioned')}
"""
        
        if dietary_restrictions:
            prompt += "Dietary Restrictions:\n"
            for restriction, value in dietary_restrictions.items():
                if value:
                    prompt += f"- {restriction.replace('_', ' ').replace('is ', '')}\n"
        elif user_data.get('dietary_restrictions'):
            prompt += f"Dietary Restrictions: {user_data.get('dietary_restrictions')}\n"
    
    prompt += "\nPrevious conversation:\n"
    recent_history = conversation_history[-5:] if len(conversation_history) > 5 else conversation_history
    for entry in recent_history:
        if entry["role"] == "user":
            prompt += f"User: {entry['message']}\n"
        else:
            prompt += f"AI: {entry['message']}\n"
    
    prompt += "\nRespond to the user's last message as a helpful fitness and nutrition coach. Remember to ONLY suggest exercises and meals from the lists provided above. When recommending meals, be careful to respect any dietary restrictions the user has mentioned:"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return f"I'm sorry, I encountered an error while generating a response. Please try again."

@ensure_csrf_cookie
def chat(request):
    """Handle chat requests"""
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    if request.method == "GET":
        conversation_history = ChatMessage.objects.filter(session_key=session_key).order_by('timestamp')
        return render(request, "LLMAgent/chat.html", {"conversation_history": conversation_history})
    
    elif request.method == "POST":
        try:
            user_message = request.POST.get("message", "")
            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)
            
            ChatMessage.objects.create(
                session_key=session_key,
                role='user',
                message=user_message
            )
            
            history = list(
                ChatMessage.objects.filter(session_key=session_key)
                .order_by('timestamp')
                .values('role', 'message')
            )
            
            ai_response = generate_fitness_response(history)
            ChatMessage.objects.create(
                session_key=session_key,
                role='ai',
                message=ai_response
            )
            
            return JsonResponse({"response": ai_response})
            
        except Exception as e:
            print(f"Error in chat view: {e}")
            print(traceback.format_exc())
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@ensure_csrf_cookie
def new_chat(request):
    """Start a new chat session"""
    if request.method == "POST":
        try:
            request.session.flush()
            request.session.create()
            session_key = request.session.session_key
            
            activity_types = FitnessActivity.objects.values_list('exercise_type', flat=True).distinct()
            activity_list = ", ".join([activity.replace('_', ' ').title() for activity in activity_types])
            
            home_meals_count = MealInstructions.objects.count()
            restaurant_count = CampusOptions_Restaurant.objects.count()
            
            welcome_message = f"""Hi! I'm your fitness and nutrition AI coach. 
            
I can help you with:
- Exercise recommendations including {activity_list}
- Nutrition advice with {home_meals_count} home cooking recipes 
- Campus dining options from {restaurant_count} nearby restaurants

Let me know your fitness goals, dietary preferences, or if you're looking for a specific type of meal!"""
            
            ChatMessage.objects.create(
                session_key=session_key,
                role='ai',
                message=welcome_message
            )
            
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(f"Error in new_chat view: {e}")
            print(traceback.format_exc())
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@ensure_csrf_cookie
def generate_fitness_plan(request):
    """Generate a personalized fitness plan based on user data"""
    if request.method == "POST":
        try:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            
            try:
                user_data = json.loads(request.body)
            except json.JSONDecodeError:
                user_data = {
                    'user_id': request.POST.get('user_id'),
                    'age': request.POST.get('age'),
                    'weight': request.POST.get('weight'),
                    'weight_unit': request.POST.get('weight_unit', 'kg'),
                    'height': request.POST.get('height'),
                    'height_unit': request.POST.get('height_unit', 'cm'),
                    'fitness_goals': request.POST.get('fitness_goals'),
                    'health_restrictions': request.POST.get('health_restrictions'),
                    'dietary_restrictions': request.POST.get('dietary_restrictions')
                }
            
            user_message = "Please create a fitness and nutrition plan based on my profile information."
            ChatMessage.objects.create(
                session_key=session_key,
                role='user',
                message=user_message
            )
            
            history = list(
                ChatMessage.objects.filter(session_key=session_key)
                .order_by('timestamp')
                .values('role', 'message')
            )
            
            ai_response = generate_fitness_response(history, user_data)
            ChatMessage.objects.create(
                session_key=session_key,
                role='ai',
                message=ai_response
            )
            
            return JsonResponse({"response": ai_response})
            
        except Exception as e:
            print(f"Error in generate_fitness_plan view: {e}")
            print(traceback.format_exc())
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@ensure_csrf_cookie
def recommend_meals(request):
    """Generate meal recommendations based on user data and dietary preferences"""
    if request.method == "POST":
        try:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            
            try:
                user_data = json.loads(request.body)
            except json.JSONDecodeError:
                user_data = {
                    'user_id': request.POST.get('user_id'),
                    'meal_type': request.POST.get('meal_type', 'any'),  
                    'calories_target': request.POST.get('calories_target'),
                    'protein_target': request.POST.get('protein_target'),
                    'dietary_restrictions': request.POST.get('dietary_restrictions')
                }
            
            user_message = f"Please recommend meals based on my dietary preferences. I'm looking for {user_data.get('meal_type', 'any')} meals."
            ChatMessage.objects.create(
                session_key=session_key,
                role='user',
                message=user_message
            )
            
            history = list(
                ChatMessage.objects.filter(session_key=session_key)
                .order_by('timestamp')
                .values('role', 'message')
            )
            
            ai_response = generate_fitness_response(history, user_data)
            ChatMessage.objects.create(
                session_key=session_key,
                role='ai',
                message=ai_response
            )
            
            return JsonResponse({"response": ai_response})
            
        except Exception as e:
            print(f"Error in recommend_meals view: {e}")
            print(traceback.format_exc())
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)