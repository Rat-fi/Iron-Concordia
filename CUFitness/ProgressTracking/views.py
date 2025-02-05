from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import Question

# Create your views here.
def index(request):
    # username = request.POST["username"]
    # password = request.POST["password"]
    # user = authenticate(request, username=username, password=password)
    latest_question_list = Question.objects.order_by("question_text")[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    output = "index"
    return HttpResponse(output)



def setGoal(request, id):
    # if request.user.is_authenticated:
    #     return HttpResponse("You logged in")
    # else:
    return HttpResponse(f"You need to log in first")
    

def result(request, question_id):
    response = "This is a testing function %s."
    return HttpResponse(response % question_id)

def detail(request, question_id):
    response = "You're looking at question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    response = "You're voting on question %s."
    return HttpResponse(response % question_id)