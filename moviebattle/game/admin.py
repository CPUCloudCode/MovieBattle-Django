from django.contrib import admin
from .models import Details, Game, Movie, Set, Entertainment

# Register your models here.
admin.site.register(Game)
admin.site.register(Movie)
admin.site.register(Set)
admin.site.register(Entertainment)
admin.site.register(Details)