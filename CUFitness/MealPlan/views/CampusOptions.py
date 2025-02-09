from django.http import JsonResponse
from django.shortcuts import render
from ..models.CampusOptions import CampusOptions_Restaurant, CampusOptions_MenuItem
from math import radians, cos, sin, asin, sqrt
import json

DEFAULT_SCHOOL_LAT = 45.4933
DEFAULT_SCHOOL_LON = -73.5781

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def campus_options(request):
    radius_km = request.GET.get('radius', 5)
    category = request.GET.get('category')
    dietary = request.GET.get('dietary') 
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')

    try:
        radius_km = float(radius_km)
    except ValueError:
        radius_km = 5

    restaurants = CampusOptions_Restaurant.objects.all()

    nearby_restaurants = []
    for restaurant in restaurants:
        distance = haversine(DEFAULT_SCHOOL_LAT, DEFAULT_SCHOOL_LON, restaurant.latitude, restaurant.longitude)
        if distance <= radius_km:
            nearby_restaurants.append(restaurant)

    
    menu_items = CampusOptions_MenuItem.objects.filter(restaurant__in=nearby_restaurants)

    if category:
        menu_items = menu_items.filter(category=category)
    if dietary:
        menu_items = menu_items.filter(dietary_restrictions=dietary)
    if max_price:
        menu_items = menu_items.filter(price__lte=max_price)
    if min_rating:
        nearby_restaurants = [r for r in nearby_restaurants if r.rating is not None and r.rating >= float(min_rating)]
    
    menu_items = menu_items.filter(restaurant__in=nearby_restaurants)

    restaurants_data = [
        {
            "name": r.name,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "rating": r.rating,
            "address": r.address,
        }
        for r in nearby_restaurants
    ]

    return render(request, 'mealplan/campus_options.html', {
    'menu_items': menu_items, 
    'radius_km': radius_km,
    'restaurants_json': json.dumps(restaurants_data),  
    })


