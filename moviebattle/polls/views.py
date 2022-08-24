from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

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

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"