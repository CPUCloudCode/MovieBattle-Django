from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('howto', views.instruction, name='howto'),
    path('about-us', views.aboutUs, name='about-us'),
    path('policy', views.policy, name='policy'),
    path('statistics', views.statistics, name='statistics'),
]