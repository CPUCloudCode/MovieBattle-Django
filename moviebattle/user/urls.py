from django.urls import path

from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.index), name='user'),
    path('settings/', login_required(views.settings), name='settings'),
    path('settings/update/', views.update, name='update'),
    path('view/<username>/', login_required(views.UserView.as_view()), name="view"),
    path('settings/updatefavourite/', views.updateFavourite, name='updatefavourite'),
    path('get/social/', login_required(views.social), name="social"),
    path('follow/', login_required(views.followUser), name="follow"),
    path('unfollow/', login_required(views.unfollowUser), name="unfollow"),
    path('createset/', login_required(views.set_create), name='createset'),
    path('postset/', login_required(views.postSet), name='postset'),
    path('get/sets/', login_required(views.sets), name="sets"),
    path('set/edit/<setId>/', login_required(views.SetEditView.as_view()), name="seteditview"),
    path('editset/', login_required(views.editSet), name='editset'),
    path('shortedit/', login_required(views.shorteditSet), name="shortedit"),
    path('delete/', login_required(views.delete), name="delete"),
]