from django.urls import path

from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.index), name='user'),
    path('settings/', login_required(views.settings), name='settings'),
    path('settings/update/', views.update, name='update'),
    path('view/<username>/', views.UserView.as_view(), name="view"),
    path('settings/updatefavourite/', views.updateFavourite, name='updatefavourite'),
]