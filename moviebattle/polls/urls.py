from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('howto', views.instruction, name='howto'),
    path('about-us', views.aboutUs, name='about-us'),
    path('policy', views.policy, name='policy'),
    path('statistics', views.statistics, name='statistics'),
    path('credit', views.credit, name='credit'),
    path("signup/", views.SignUp.as_view(), name="signup"),
]