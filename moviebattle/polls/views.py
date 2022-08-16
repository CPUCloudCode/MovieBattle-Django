from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader

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