import json
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
            userView = User.objects.get(username=user)
            data['userview'] = userView
            details = Details.objects.get(user=request.user)
            if str(details.social).__contains__(str(userView.id)):
                data['following'] = True
            else:
                data['following'] = False
        else:
            logger.warning("User not exists!")
            return redirect('/user/')
        
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

def social(request):
    
    logger.warning("Social-------------------")
    logger.warning("UserID: " + str(request.user.id))
    logger.warning("User: " + str(request.user))
    context = {"friend": str(request.user)}

    details = Details.objects.get(user=request.user)

    social = details.social
    
    split = social.split(';')
    sp = "1;2;3;4;5"
    #split = sp.split(';')
    logger.warning("Split: " + str(split))
    users = []
    multi = 1
    if split:
        for id in split:
            if id and id != '':
                if User.objects.filter(id=id).exists():
                    user = User.objects.get(id=id)
                    if Details.objects.filter(user=user).exists():
                        details = Details.objects.get(user=user)
                        logger.warning('Details: ' + str(details.profile_image))
                        userJson = {"username": str(user.username), "avatar": str(details.profile_image)}
                    else:
                        userJson = {"username": str(user.username), "avatar": "https://wallpaperaccess.com/full/4595683.jpg"}
                    users.append(userJson)
                    logger.warning("Friend: " + str(userJson))
                    multi+=1
            else:
                logger.warning("ID is empty")
    context['len'] = len(users)  
    context['users'] = users
    logger.warning("Context: " + str(context)) 
    return JsonResponse(context)

def followUser(request):
    logger.warning("Follow User activated--------------------")

    user = User.objects.get(username=request.POST['username'])

    details = Details.objects.get(user=request.user)

    logger.warning("SocialBEFORE: " + str(details.social))

    social = str(details.social)

    if not social.__contains__(str(user.id)):
        socialStr = str(user.id) + ";"
        social = social + socialStr
        details.social = social
        details.save()
    logger.warning("SocialAFTER: " + str(details.social))

    return JsonResponse({"failed": "false"})

def unfollowUser(request):
    logger.warning("UnFollow User activated-------------------")

    user = User.objects.get(username=request.POST['username'])

    details = Details.objects.get(user=request.user)


    social = details.social
    split = social.split(';')
    split.remove(str(user.id))
    prime = ""
    for s in split:
        if s and s != '':
            primeStr = s + ";"
            prime = prime + primeStr
    details.social = prime
    details.save()

    return JsonResponse({"failed": "false"})

