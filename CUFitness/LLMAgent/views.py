from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import ChatMessage
from ProgressTracking.models import FitnessActivity
from MealPlan.models.DietaryRestrictions import DietaryRestrictions, DietaryRestrictions_MealPlan
from MealPlan.models.QuickMeal import QuickMeal
from MealPlan.models.NewCookUser import MealInstructions
from MealPlan.models.CampusOptions import CampusOptions_MenuItem, CampusOptions_Restaurant
from .models import FitnessPlan
from ProgressTracking.models import GymGoal
import google.generativeai as genai
import os
from dotenv import load_dotenv
import traceback
import json
import re


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
    
    prompt += "\nRestaurant Options:\n"
    prompt += restaurant_text
    
    if user_data and user_data.get('user_id'):
        try:
            last_plan = FitnessPlan.objects.filter(user_id=user_data['user_id'], confirmed=True).latest('created_at')
            prompt += "\nPrevious Confirmed Fitness Plan:\n"
            prompt += last_plan.plan_content + "\n"
        except FitnessPlan.DoesNotExist:
            prompt += "\n(No previous confirmed plan found.)\n"
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
    
    prompt += """
Now respond to the user based on their last question.
Keep your reply structured and helpful.

End your reply by asking if they're satisfied with the plan, and remind them they can confirm it.
"""

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
        if request.user.is_authenticated:
            conversation_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
        else:
            conversation_history = ChatMessage.objects.filter(session_key=session_key).order_by('timestamp')
        return render(request, "LLMAgent/chat.html", {"conversation_history": conversation_history})

    elif request.method == "POST":
        try:
            user_message = request.POST.get("message", "")
            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)
            
            if request.user.is_authenticated and user_message.strip().lower() == "confirm plan":
                last_plan = FitnessPlan.objects.filter(user=request.user, confirmed=False).order_by('-created_at').first()

                if not last_plan:
                    # Even if already confirmed or not found, exit here
                    return JsonResponse({"response": "⚠️ No unconfirmed fitness plan found. Please generate a new one first."})

                goal, _ = GymGoal.objects.get_or_create(user=request.user)

                all_exercises = [
                    'cardio', 'weight_lifting', 'yoga', 'pilates', 'hiit', 'cycling', 'swimming',
                    'running', 'rowing', 'boxing', 'dancing', 'strength_training', 'crossfit',
                    'stretching', 'elliptical_trainer', 'kickboxing', 'calisthenics', 'tai_chi',
                    'mountain_climbers', 'trx_training', 'power_yoga', 'hiking', 'sled_push',
                    'water_aerobics', 'zumba', 'jump_rope'
                ]

                plan_lower = last_plan.plan_content.lower()
                updated = False

                for exercise in all_exercises:
                    pattern = rf"{exercise}.*?(\d+)\s*minutes"
                    match = re.search(pattern, plan_lower)
                    if match:
                        duration = int(match.group(1))
                        current_value = getattr(goal, exercise, 0)
                        setattr(goal, exercise, current_value + duration)
                        updated = True
                        print(f"[DEBUG] {exercise}: +{duration} ➜ {current_value + duration}")

                if updated:
                    goal.save()
                    print("[DEBUG] ✅ GymGoal saved with durations from confirmed plan.")
                else:
                    print("[DEBUG] ⚠️ Plan confirmed but no exercises found.")

                last_plan.confirmed = True
                last_plan.save()

                ChatMessage.objects.create(
                    session_key=session_key,
                    user=request.user,
                    role='ai',
                    message="✅ Your fitness plan has been confirmed and saved to your Gym Goals! Let's keep it up!"
                )

                return JsonResponse({"response": "✅ Plan confirmed and saved to Gym Goals!"})  # 👈 THIS stops it from continuing




            ChatMessage.objects.create(
                session_key=session_key,
                user=request.user if request.user.is_authenticated else None,
                role='user',
                message=user_message
            )

            if request.user.is_authenticated:
                history = list(
                    ChatMessage.objects.filter(user=request.user).order_by('timestamp').values('role', 'message')
                )
            else:
                history = list(
                    ChatMessage.objects.filter(session_key=session_key).order_by('timestamp').values('role', 'message')
                )

            ai_response = generate_fitness_response(history)
            if not any(x in ai_response.lower() for x in [
                    "reply with 'confirm plan'",
                    "reply 'confirm plan'",
                    "respond with 'confirm plan'"
                ]):
                ai_response += "\n\n❓ Are you satisfied with this fitness plan? Reply with 'confirm plan' if you want me to save it as your official Gym Goal."
            if request.user.is_authenticated and "workout plan" in ai_response.lower() and "nutrition plan" in ai_response.lower():
                FitnessPlan.objects.create(user=request.user, plan_content=ai_response)
                print("[DEBUG] Saved new unconfirmed FitnessPlan.")
            ChatMessage.objects.create(
                session_key=session_key,
                user=request.user if request.user.is_authenticated else None,
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
            if not request.session.session_key:
                request.session.create()
            else:
                request.session.modified = True

            session_key = request.session.session_key

            # 💥 Delete old chat messages for the user or session
            if request.user.is_authenticated:
                ChatMessage.objects.filter(user=request.user).delete()
            else:
                ChatMessage.objects.filter(session_key=session_key).delete()

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
                user=request.user if request.user.is_authenticated else None,
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
                user=request.user if request.user.is_authenticated else None,
                role='user',
                message=user_message
            )

            if request.user.is_authenticated:
                history = list(
                    ChatMessage.objects.filter(user=request.user).order_by('timestamp').values('role', 'message')
                )
            else:
                history = list(
                    ChatMessage.objects.filter(session_key=session_key).order_by('timestamp').values('role', 'message')
                )

            ai_response = generate_fitness_response(history, user_data)
            ChatMessage.objects.create(
                session_key=session_key,
                user=request.user if request.user.is_authenticated else None,
                role='ai',
                message=ai_response
            )

            # Store plan in DB as unconfirmed
            if request.user.is_authenticated:
                from .models import FitnessPlan
                FitnessPlan.objects.create(user=request.user, plan_content=ai_response)

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
                user=request.user if request.user.is_authenticated else None,
                role='user',
                message=user_message
            )

            if request.user.is_authenticated:
                history = list(
                    ChatMessage.objects.filter(user=request.user).order_by('timestamp').values('role', 'message')
                )
            else:
                history = list(
                    ChatMessage.objects.filter(session_key=session_key).order_by('timestamp').values('role', 'message')
                )

            ai_response = generate_fitness_response(history, user_data)
            ChatMessage.objects.create(
                session_key=session_key,
                user=request.user if request.user.is_authenticated else None,
                role='ai',
                message=ai_response
            )

            return JsonResponse({"response": ai_response})

        except Exception as e:
            print(f"Error in recommend_meals view: {e}")
            print(traceback.format_exc())
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
