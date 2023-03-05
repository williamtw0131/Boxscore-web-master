from django import forms
from .models import Boxscore

class BoxscoreForm(forms.ModelForm):
    class Meta:
        model = Boxscore
        fields = ('team_name', 'player', 'fgm', 'fga', 'threepm', 'threepa', 'ftm', 'fta', 'oreb', 'dreb', 'ast', 'stl', 'blk', 'tov', 'pf')
