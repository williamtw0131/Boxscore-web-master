from django.contrib import admin
from .models import Boxscore, Team, Game, Lifetime

# Register your models here.

admin.site.register(Boxscore)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Lifetime)
