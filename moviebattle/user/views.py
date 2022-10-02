from django.utils import timezone
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from game.models import Details, Set
import logging
from django.views.generic import View
from django.contrib.auth.models import User
logger = logging.getLogger(__name__)

# Create your views here. 

def index(request):
    
    template = loader.get_template('user/user.html')
    current_user = request.user
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

def set_create(request):

    template = loader.get_template('user/user_set_create.html')
        
    return HttpResponse(template.render({}, request))

def postSet(request):
    title = request.POST.get('title')
    desc = request.POST.get('desc')
    poster = request.POST.get('poster')
    titles = request.POST.getlist('titles')
    posters = request.POST.getlist('posters')

    logger.warning("Title: " + str(title))
    logger.warning("Desc: " + str(desc))
    logger.warning("Poster: " + str(poster))
    logger.warning("Titles: " + str(titles))
    logger.warning("Posters: " + str(posters))
    
    user = str(request.user)
    set = Set(pub_date=timezone.now(), creator=user, title=title, poster=poster, description=desc)
    set.save()
    for i in range(len(titles)):
        set.entertainment_set.create(title = titles[i], href = posters[i])

    data = {}


    return JsonResponse(data)

def sets(request):
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        sets = Set.objects.filter(creator=request.user).values()
        ren = []
        for set in sets:
            setView = Set.objects.get(id=set["id"])
            logger.warning(setView)
            object = {"id": str(set['id']),
             "title": str(set['title']), 
             "poster": str(set['poster']),
             "description": str(set['description']),
             "public": set['public'],
             "length": len(setView.entertainment_set.all())
             }
            ren.append(object)
        logger.warning("Ren: " + str(ren))
        return JsonResponse({"test": ren}, status = 200)

    return JsonResponse({}, status = 400)

class SetEditView(View):
    def get(self, request, *args, **kwargs):

        setId = kwargs['setId']

        data = {}
        logger.warning("Set Edit")
        if Set.objects.filter(id=setId):
            logger.warning("Set exists!")
            setView = Set.objects.get(id=setId)
            data['set'] = setView
            data['entertainments'] = setView.entertainment_set.all()
        else:
            logger.warning("Set does not exists!")
            return redirect('/user/')
        
        return render(request, 'user/user_set_edit.html', data)

def editSet(request):
    title = request.POST.get('title')
    desc = request.POST.get('desc')
    poster = request.POST.get('poster')
    titles = request.POST.getlist('titles')
    posters = request.POST.getlist('posters')
    id = request.POST.get('id')

    
    user = str(request.user)
    context = {}
    context["test"] = "Lol"
    if Set.objects.filter(id=id, creator=user):
            logger.warning("Set exists!")
            set = Set.objects.get(id=id, creator=user)
            set.title = title
            set.poster = poster
            set.description = desc

            set.save()
            # Delete all former entertainments
            for entertainment in set.entertainment_set.all():
                entertainment.delete()
            # Then add all current entertainments
            for i in range(len(titles)):
                set.entertainment_set.create(title = titles[i], href = posters[i])
            context["updated"] = True
    else:
        logger.warning("Set does not exists!")
        context["updated"] = False
    

    return JsonResponse(context)

def shorteditSet(request):
    title = request.POST.get('title')
    desc = request.POST.get('description')
    poster = request.POST.get('poster')
    public = request.POST.get('public')
    id = request.POST.get('id')

    user = str(request.user)
    context = {}
    if Set.objects.filter(id=id, creator=user):
            logger.warning("Set exists!")
            set = Set.objects.get(id=id, creator=user)
            set.title = title
            set.poster = poster
            set.description = desc
            length = len(set.entertainment_set.all())
            if length>=8:
                if public == "true":
                    set.public = True
                else:
                    set.public = False

            set.save()
            # Delete all former entertainments
            context["updated"] = True
            context["id"] = id
            context["desc"] = desc
            context["title"] = title
            context["poster"] = poster
            context["public"] = set.public
            context["length"] = length
    else:
        logger.warning("Set does not exists!")
        context["updated"] = False
    

    return JsonResponse(context)

def delete(request):
    id = request.POST.get('id')

    user = str(request.user)
    context = {}
    if Set.objects.filter(id=id, creator=user):
            logger.warning("Set exists!")
            set = Set.objects.get(id=id, creator=user)
            context["id"] = set.id
            set.delete()
            # Delete all former entertainments
            context["deleted"] = True

    else:
        logger.warning("Set does not exists!")
        context["deleted"] = False
    

    return JsonResponse(context)