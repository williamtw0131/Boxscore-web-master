from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import Boxscore, Team, Game, Lifetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        email = request.POST.get('email')
        # if any one of above wasn't fill in
        if not username or not raw_password or not email:
            return render(request, 'boxscore/register.html', {'error': "Please fill in all of the blanks."})
        # if username or email was already signed
        elif User.objects.filter(username=username) or User.objects.filter(email=email):
            return render(request, 'boxscore/register.html', {'error': "username or email used."})

        else:
            user = User.objects.create_user(username, email, raw_password)
            user = authenticate(username=username, password=raw_password) # log user in right after successfully registered
            login(request, user)
            return render(request, 'boxscore/statics.html', {'succeed': "Registered!"})
    else:
        return render(request, 'boxscore/register.html')

@login_required
def stat(request):
    my_statics = Boxscore.objects.filter(user=request.user).order_by('team_name', 'opponent', 'player') # all of the statistics under this user
    return render(request, 'boxscore/statics.html', {'my_statics': my_statics})

@login_required
def team_boxscore(request, team_name):
    statics = Boxscore.objects.filter(user=request.user, team_name=team_name).order_by('opponent', 'player')
    if not statics:
        statics = Team.objects.filter(team_cap=request.user).order_by('team_name_under_Team')
        return render(request, 'boxscore/add_game.html', {'statics': statics, 'succeed': "Successfully signed up a team. Now updates games for it."})
    else:
        team_name = statics.values()[0]['team_name']
        return render(request, 'boxscore/team_boxscore.html', {'statics': statics, 'team_name': team_name})

@login_required
def match_boxscore(request, team_name, opponent):
    statics = Boxscore.objects.filter(user=request.user, team_name=team_name, opponent=opponent).order_by('player')
    return render(request, 'boxscore/match_boxscore.html', {'statics': statics, 'team_name': team_name, 'opponent': opponent})

@login_required
def add_stat(request):
    if request.method == "POST":
        user = request.user
        game_id = request.POST.get('game_name')
        player = request.POST.get('player')
        if not game_id or not player:
            game_list = Game.objects.filter(user_under_game=request.user)
            return render(request, 'boxscore/add_stat.html', {'error': "Please select a game and input player number.", 'game_list': game_list})
        game_info = Game.objects.filter(id=game_id).values()
        team_name = game_info[0]['us']
        opponent = game_info[0]['opponent']
        if Boxscore.objects.filter(user=user, team_name=team_name, opponent=opponent, player=player):
            # if the stat was already exist
            game_list = Game.objects.filter(user_under_game=request.user)
            return render(request, 'boxscore/add_stat.html', {'error': "Stat of player # %s at this match was added." % (player), 'game_list': game_list})
        fgm = request.POST.get('fgm')
        fga = request.POST.get('fga')
        threepm = request.POST.get('threepm')
        threepa = request.POST.get('threepa')
        ftm = request.POST.get('ftm')
        fta = request.POST.get('fta')
        if int(fgm) > int(fga) or int(threepm) > int(threepa) or int(ftm) > int(fta):
            game_list = Game.objects.filter(user_under_game=request.user)
            return render(request, 'boxscore/add_stat.html', {'error': "Attempt shooting can't be more than make. Please try again.", 'game_list': game_list})
        oreb = request.POST.get('oreb')
        dreb = request.POST.get('dreb')
        ast = request.POST.get('ast')
        stl = request.POST.get('stl')
        blk = request.POST.get('blk')
        tov = request.POST.get('tov')
        pf = request.POST.get('pf')
        Boxscore.objects.create(user=user, team_name=team_name, opponent=opponent, player=player, fgm=fgm, fga=fga, threepm=threepm, threepa=threepa, ftm=ftm, fta=fta, oreb=oreb, dreb=dreb, ast=ast, stl=stl, blk=blk, tov=tov, pf=pf)
        if Lifetime.objects.filter(user=user, team_name=team_name, player=player):
            # if this player was already in the system, add up the new stat in his lifetime record
            lifetime = Lifetime.objects.get(user=user, team_name=team_name, player=player)
            lifetime.fgm += int(fgm)
            lifetime.fga += int(fga)
            lifetime.threepm += int(threepm)
            lifetime.threepa += int(threepa)
            lifetime.ftm += int(ftm)
            lifetime.fta += int(fta)
            lifetime.oreb += int(oreb)
            lifetime.dreb += int(dreb)
            lifetime.ast += int(ast)
            lifetime.stl += int(stl)
            lifetime.blk += int(blk)
            lifetime.tov += int(tov)
            lifetime.pf += int(pf)
            lifetime.games += 1
            lifetime.save()
        else:
            Lifetime.objects.create(user=user, team_name=team_name, player=player, fgm=fgm, fga=fga, threepm=threepm, threepa=threepa, ftm=ftm, fta=fta, oreb=oreb, dreb=dreb, ast=ast, stl=stl, blk=blk, tov=tov, pf=pf, games=1)
        return redirect('team_boxscore', team_name=team_name)
    else:
        game_list = Game.objects.filter(user_under_game=request.user)
        return render(request, 'boxscore/add_stat.html', {'game_list': game_list})

@login_required
def search(request):
    if request.method == "POST":
        search_by_team_name = request.POST.get('search_by_team_name')
        search_by_player = request.POST.get('search_by_player')
        if not search_by_team_name and not search_by_player:
            statics = Team.objects.filter(team_cap=request.user).order_by('team_name_under_Team')
            return render(request, 'boxscore/search.html', {'statics': statics, 'error': "Please at least select a match or a team name or input a player number."})
        else:
            if not search_by_player:
                statics = Boxscore.objects.filter(user=request.user, team_name=search_by_team_name).order_by('opponent', 'player')
            elif not search_by_team_name:
                statics = Boxscore.objects.filter(user=request.user, player=search_by_player).order_by('opponent')
            else:
                statics = Boxscore.objects.filter(user=request.user, team_name=search_by_team_name, player=search_by_player).order_by('opponent')
            return render(request, 'boxscore/result.html', {'statics': statics})
    else:
        statics = Team.objects.filter(team_cap=request.user).order_by('team_name_under_Team')
        return render(request, 'boxscore/search.html', {'statics': statics})

@login_required
def team_signup(request):
    if request.method == "POST":
        team_name_under_Team = request.POST.get('team_name')
        if not team_name_under_Team:
            return render(request, 'boxscore/team_signup.html', {'error': "Please enter team name."})
        elif Team.objects.filter(team_cap=request.user, team_name_under_Team=team_name_under_Team):
            return render(request, 'boxscore/team_signup.html', {'error': "This name \'%s\' was already signed up by you." % (team_name_under_Team)})
        else:
            Team.objects.create(team_cap=request.user, team_name_under_Team=team_name_under_Team)
            return redirect('team_boxscore', team_name=team_name_under_Team)# render(request, 'boxscore/team_signup.html')
    else:
        return render(request, 'boxscore/team_signup.html')

@login_required
def games(request):
    games = Game.objects.filter(user_under_game=request.user)
    return render(request, 'boxscore/games.html', {'games': games})

@login_required
def add_game(request):
    if request.method == "POST":
        us = request.POST.get('us')
        opponent = request.POST.get('opponent')
        statics = Team.objects.filter(team_cap=request.user).order_by('team_name_under_Team')
        if not us or not opponent:
            return render(request, 'boxscore/add_game.html', {'statics': statics, 'error': "Please select your team name and fill in the blank."})
        elif Game.objects.filter(user_under_game=request.user, us=us, opponent=opponent):
            return render(request, 'boxscore/add_game.html', {'statics': statics, 'error': "You already updated this match."})
        else:
            Game.objects.create(user_under_game=request.user, us=us, opponent=opponent)
            games = Game.objects.filter(user_under_game=request.user)
            return render(request, 'boxscore/games.html', {'games': games})
    else:
        statics = Team.objects.filter(team_cap=request.user).order_by('team_name_under_Team')
        return render(request, 'boxscore/add_game.html', {'statics': statics})


@login_required
def ave(request, team_name):
    statics = Lifetime.objects.filter(user=request.user, team_name=team_name).order_by('player')
    return render(request, 'boxscore/ave.html', {'statics': statics, 'team_name': team_name})

@login_required
def edit(request):
    if request.method == "POST":
        pk = request.POST.get('pk')
        stat = Boxscore.objects.filter(pk=pk)
        return render(request, 'boxscore/edit_stat.html', {'stat': stat})
    else:
        statics = Boxscore.objects.filter(user=request.user).order_by('opponent', 'player')
        return render(request, 'boxscore/edit.html', {'statics': statics})

@login_required
def delete(request, pk, team_name, player):
    if request.method == "POST":
        old_stat = Boxscore.objects.filter(pk=pk)
        lifetime = Lifetime.objects.filter(user=request.user, team_name=team_name, player=player)
        new_fgm = lifetime.values()[0]['fgm'] - old_stat.values()[0]['fgm']
        new_fga = lifetime.values()[0]['fga'] - old_stat.values()[0]['fga']
        new_threepm = lifetime.values()[0]['threepm'] - old_stat.values()[0]['threepm']
        new_threepa = lifetime.values()[0]['threepa'] - old_stat.values()[0]['threepa']
        new_ftm = lifetime.values()[0]['ftm'] - old_stat.values()[0]['ftm']
        new_fta = lifetime.values()[0]['fta'] - old_stat.values()[0]['fta']
        new_oreb = lifetime.values()[0]['oreb'] - old_stat.values()[0]['oreb']
        new_derb = lifetime.values()[0]['dreb'] - old_stat.values()[0]['dreb']
        new_ast = lifetime.values()[0]['ast'] - old_stat.values()[0]['ast']
        new_stl = lifetime.values()[0]['stl'] - old_stat.values()[0]['stl']
        new_blk = lifetime.values()[0]['blk'] - old_stat.values()[0]['blk']
        new_tov = lifetime.values()[0]['tov'] - old_stat.values()[0]['tov']
        new_pf = lifetime.values()[0]['pf'] - old_stat.values()[0]['pf']
        old_stat.delete()
        lifetime.update(fgm=new_fgm, fga=new_fga, threepm=new_threepm, threepa=new_threepa, ftm=new_ftm, fta=new_fta, oreb=new_oreb, dreb=new_derb, ast=new_ast, stl=new_stl, blk=new_blk, tov=new_tov, pf=new_pf)
        return redirect('stat')
    else:
        stat = Boxscore.objects.filter(pk=pk).order_by('opponent', 'player')
        return render(request, 'boxscore/delete.html', {'stat': stat})

@login_required
def edit_stat(request, pk, team_name, player):
    if request.method == "POST":
        fgm = request.POST.get('fgm')
        fga = request.POST.get('fga')
        threepm = request.POST.get('threepm')
        threepa = request.POST.get('threepa')
        ftm = request.POST.get('ftm')
        fta = request.POST.get('fta')
        if int(fgm) > int(fga) or int(threepm) > int(threepa) or int(ftm) > int(fta):
            stat = Boxscore.objects.filter(pk=pk).order_by('opponent', 'player')
            return render(request, 'boxscore/edit_stat.html', {'error': "Attempt shooting can't be more than make. Please try again.", 'stat': stat})
        # edit the lifetime record
        old_stat = Boxscore.objects.filter(pk=pk)
        lifetime = Lifetime.objects.filter(user=request.user, team_name=team_name, player=player)
        oreb = request.POST.get('oreb')
        dreb = request.POST.get('dreb')
        ast = request.POST.get('ast')
        stl = request.POST.get('stl')
        blk = request.POST.get('blk')
        tov = request.POST.get('tov')
        pf = request.POST.get('pf')
        new_fgm = lifetime.values()[0]['fgm'] - old_stat.values()[0]['fgm'] + int(fgm)
        new_fga = lifetime.values()[0]['fga'] - old_stat.values()[0]['fga'] + int(fga)
        new_threepm = lifetime.values()[0]['threepm'] - old_stat.values()[0]['threepm'] + int(threepm)
        new_threepa = lifetime.values()[0]['threepa'] - old_stat.values()[0]['threepa'] + int(threepa)
        new_ftm = lifetime.values()[0]['ftm'] - old_stat.values()[0]['ftm'] + int(ftm)
        new_fta = lifetime.values()[0]['fta'] - old_stat.values()[0]['fta'] + int(fta)
        new_oreb = lifetime.values()[0]['oreb'] - old_stat.values()[0]['oreb'] + int(oreb)
        new_derb = lifetime.values()[0]['dreb'] - old_stat.values()[0]['dreb'] + int(dreb)
        new_ast = lifetime.values()[0]['ast'] - old_stat.values()[0]['ast'] + int(ast)
        new_stl = lifetime.values()[0]['stl'] - old_stat.values()[0]['stl'] + int(stl)
        new_blk = lifetime.values()[0]['blk'] - old_stat.values()[0]['blk'] + int(blk)
        new_tov = lifetime.values()[0]['tov'] - old_stat.values()[0]['tov'] + int(tov)
        new_pf = lifetime.values()[0]['pf'] - old_stat.values()[0]['pf'] + int(pf)
        old_stat.update(fgm=fgm, fga=fga, threepm=threepm, threepa=threepa, ftm=ftm, fta=fta, oreb=oreb, dreb=dreb, ast=ast, stl=stl, blk=blk, tov=tov, pf=pf)
        lifetime.update(fgm=new_fgm, fga=new_fga, threepm=new_threepm, threepa=new_threepa, ftm=new_ftm, fta=new_fta, oreb=new_oreb, dreb=new_derb, ast=new_ast, stl=new_stl, blk=new_blk, tov=new_tov, pf=new_pf)
        return redirect('stat')
    else:
        stat = Boxscore.objects.filter(pk=pk).order_by('opponent', 'player')
        return render(request, 'boxscore/edit_stat.html', {'stat': stat})
