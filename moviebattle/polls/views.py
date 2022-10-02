from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from game.models import Details, Set, Game, Entertainment
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    
    template = loader.get_template('polls/index.html')
    return HttpResponse(template.render({}, request))

def instruction(request):
    
    template = loader.get_template('polls/instruction.html')
    return HttpResponse(template.render({}, request))

def aboutUs(request):
    
    template = loader.get_template('polls/about-us.html')
    return HttpResponse(template.render({}, request))

def policy(request):
    
    template = loader.get_template('polls/policy.html')
    return HttpResponse(template.render({}, request))

def statistics(request):
    
    template = loader.get_template('polls/statistics.html')
    return HttpResponse(template.render({}, request))

def credit(request):
    
    template = loader.get_template('polls/credit.html')
    return HttpResponse(template.render({}, request))

def sitestats(request):
    
    data = {
        "users": len(User.objects.all().values()),
        "sets": len(Set.objects.all().values()),
        "open_games": len(Game.objects.all().values()),
        "entertainments": len(Entertainment.objects.all().values()),
        "moderator": len(Details.objects.filter(moderator=True).values()),
        "premium": len(Details.objects.filter(premium=True).values()),
    }

    template = loader.get_template('polls/sitestats.html')
    return HttpResponse(template.render(data, request))

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"