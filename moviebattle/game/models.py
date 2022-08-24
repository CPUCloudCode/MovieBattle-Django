import unicodedata
from django.db import models
import uuid
from django.db import models
from django.utils import timezone
import datetime
import ast
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pub_date = models.DateTimeField('date published')
    rounds = models.IntegerField(default=4)
    round = models.IntegerField(default=1)
    started = models.BooleanField(default=False)
    vote = models.BooleanField(default=False)
    c1 = models.CharField(max_length=50, default="")
    c2 = models.CharField(max_length=50, default="")

    def __str__(self):
        return str(self.id)
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Movie(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    movie_text = models.CharField(max_length=200)
    active = models.IntegerField(default=1) 
    user = models.CharField(max_length=200, default="")
    href = models.CharField(max_length=200, default="")
    votes = models.IntegerField(default=0) 

    def __str__(self):
        return self.movie_text


class Voter(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    voted = models.BooleanField(default=True)

    def __str__(self):
        return self.ip_address

class MovieSaved(models.Model):
    title = models.CharField(max_length=200, unique=True)
    wins = models.IntegerField(default=1)
    votes = models.IntegerField(default=1)

class Set(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pub_date = models.DateTimeField('date published')
    plays = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    creator = models.CharField(max_length=50, default="")
    description = models.TextField(default="")
    title = models.CharField(max_length=20, default="")
    poster = models.CharField(max_length=300, default="")

    def __str__(self):
        return str(self.id)
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Entertainment(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    title = models.CharField(max_length=200) 
    href = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.title

class Details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(default="Hey there, this is my profile on Movie-Contest.live")
    profile_image = models.ImageField(upload_to='profile_images')
    background_image = models.ImageField(upload_to='background_images')
    premium = models.BooleanField(default=False)
    moderator = models.BooleanField(default=False)
    favourite_movie = models.CharField(max_length=200, default="")
    favourite_series = models.CharField(max_length=200, default="")
    def delete(self, using=None, keep_parents=False):
        self.profile_image.storage.delete(self.profile_image.name)
        self.background_image.storage.delete(self.background_image.name)
        
    def delete_Avatar(self, using=None, keep_parents=False):
        self.profile_image.storage.delete(self.profile_image.name)
        
    def delete_Banner(self, using=None, keep_parents=False):
        self.background_image.storage.delete(self.background_image.name)
        