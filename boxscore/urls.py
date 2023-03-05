from django.urls import path
from .import views

urlpatterns = [
    path('', views.stat, name='stat'),
    path('stat/<team_name>/', views.team_boxscore, name='team_boxscore'),
    path('stat/match_of/<team_name>/<opponent>/', views.match_boxscore, name='match_boxscore'),
    path('stat/add_stat', views.add_stat, name='add_stat'),
    path('stat/search', views.search, name='search'),
    path('stat/register', views.register, name='register'),
    path('stat/team_signup', views.team_signup, name='team_signup'),
    path('stat/games', views.games, name='games'),
    path('stat/add_game', views.add_game, name='add_game'),
    path('stat/<team_name>ave', views.ave, name='ave'),
    path('stat/edit', views.edit, name='edit'),
    path('stat/edit_stat<pk>_<team_name>_<player>', views.edit_stat, name='edit_stat'),
    path('stat/delete<pk>_<team_name>_<player>', views.delete, name='delete'),
]
