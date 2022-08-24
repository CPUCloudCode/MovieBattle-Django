from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from game.models import Details
import logging
from django.views.generic import View
from django.contrib.auth.models import User
logger = logging.getLogger(__name__)

# Create your views here. 

def index(request):
    
    template = loader.get_template('user/user.html')
    current_user = request.user
    logger.warning("---------------------------------------")
    logger.warning("User: " + str(current_user))
    logger.warning("Filter: " + str(Details.objects.filter(user=current_user)))
    if not Details.objects.filter(user=current_user):
        Details.objects.create(user=current_user)
        

    return HttpResponse(template.render({}, request))

class UserView(View):
    def get(self, request, *args, **kwargs):

        user = kwargs['username']

        data = {}
        logger.warning("Search User")
        if User.objects.filter(username=user):
            logger.warning("User exists!")
            data['userview'] = User.objects.get(username=user)
        else:
            logger.warning("User not exists!")
        
        return render(request, 'user/user_view.html', data)

def settings(request):
    
    template = loader.get_template('user/settings.html')
    current_user = request.user
    logger.warning("---------------------------------------")
    
    if not Details.objects.filter(user=current_user):
        Details.objects.create(user=current_user)
        
    
    return HttpResponse(template.render({}, request))

def update(request):
    
    logger.warning("Lol-------------------")
   
    context = {"test": "success"}

    avatar = None
    banner = None
    keys = list(request.FILES.keys())
    if 'formFileAvatar' in keys:
        avatar = request.FILES['formFileAvatar']
    if 'formFileBanner' in keys:
        banner = request.FILES['formFileBanner']

    details = Details.objects.get(user=request.user)
    
    if avatar and banner:
        logger.warning("")
        if details.profile_image and details.background_image:
            details.delete()
            details.profile_image = avatar
            details.background_image = banner
        else:
            if details.profile_image:
                details.delete_Avatar()
            details.profile_image = avatar
            if details.background_image:
                details.delete_Banner()
            details.background_image = banner
    else:
        if avatar:
            if details.profile_image:
                details.delete_Avatar()
            details.profile_image = avatar
        if banner:
            if details.background_image:
                details.delete_Banner()
            details.background_image = banner
    details.description = request.POST['description']
    details.save()
    

    logger.warning("WOOOW sooo simple maate")
    #return settings(request)
    template = loader.get_template('user/settings.html')
        

    return redirect('settings')


def updateFavourite(request):
    
    logger.warning("Lol-------------------")
   
    context = {"test": "success"}

    details = Details.objects.get(user=request.user)

    details.favourite_movie = request.POST['movie']
    details.favourite_series = request.POST['series']

    details.save()
        
    return JsonResponse(context)