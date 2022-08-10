import unicodedata
from django.db import models
import uuid
from django.db import models
from django.utils import timezone
import datetime
import ast

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