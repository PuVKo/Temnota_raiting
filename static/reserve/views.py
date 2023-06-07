from django.shortcuts import render
from django.http import HttpResponse
from .models import Raiting, Game, Season, Player, FullSeason
from django.db.models import F, IntegerField, ExpressionWrapper, Sum, FloatField, Q
from datetime import datetime
from datetime import date
import hashlib

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.db.models import Max

from typing import Tuple, Dict
from django.db.models import QuerySet

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

#Проверка прав пользователя
def staff_check(user):
    return user.is_staff

#Если пользователь не имеет статуса персонала отправить на страницу access_denied
def staff_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not staff_check(request.user):
            return redirect('access_denied')
        return view_func(request, *args, **kwargs)
    return wrapper

#Отображение страницы access denied
def access_denied_view(request):
    return render (request, 'access_denied.html', {'title': 'Доступ запрещен'}) 

#Функция выборки сезона, используется для главной страницы и списка игр на админке
def get_month_and_gamecounter(request):
    months = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь',
    }
    
    if request.method == 'POST':
        if request.POST.get('type') == 'season':
            now = request.POST.get('selected_option')
            month = 'Весна'
            now1 = FullSeason.objects.get(pk=int(now)).date1
            now2 = FullSeason.objects.get(pk=int(now)).date2
            now3 = FullSeason.objects.get(pk=int(now)).date3
            month1 = now1.month
            month2 = now2.month
            month3 = now3.month
            currectmonth = ''
            currectyear = now1.year
        else:
            if request.POST.get('selected_option') == 'none':
                now = datetime.now()
                currectmonth = now.month
                currectyear = now.year
                month = months.get(currectmonth)
                month1 = ''
                month2 = ''
                month3 = ''
            else:
                now = request.POST.get('selected_option')
                now = Season.objects.get(pk=int(now)).date
                currectmonth = now.month
                currectyear = now.year
                month = months.get(currectmonth)
                month1 = ''
                month2 = ''
                month3 = ''
    else:
        now = datetime.now()
        currectmonth = now.month
        currectyear = now.year
        month = months.get(currectmonth)
        month1 = ''
        month2 = ''
        month3 = ''
    
    fullseason = FullSeason.objects.all().order_by('-date1')
    season = Season.objects.all().order_by('-date')
    
    if request.method == 'POST':
        if request.POST.get('type') == 'season':
            gamecounter = Game.objects.filter(gamedate__month=month1, gamedate__year=currectyear).count()
            gamecounter = gamecounter + Game.objects.filter(gamedate__month=month2, gamedate__year=currectyear).count()
            gamecounter = gamecounter + Game.objects.filter(gamedate__month=month3, gamedate__year=currectyear).count()
        else:
            gamecounter = Game.objects.filter(gamedate__month=currectmonth, gamedate__year=currectyear).count()
    else:
        gamecounter = Game.objects.filter(gamedate__month=currectmonth, gamedate__year=currectyear).count()

    return month, gamecounter, season, currectyear, currectmonth, fullseason, month1, month2, month3

#Функция выборки игр по сезонам, используется для страниц просмотра всех игр
def games_selector(request, games):
    winnerpool = {
            'mir': 'Мирные',
            'maf': 'Мафия',
    }
    rolepool = {
            'mir': 'Мирный',
            'maf': 'Мафия',
            'don': 'Дон',
            'ser': 'Шериф',
    }
    month, gamecounter, season, currectyear, currectmonth, fullseason, month1, month2, month3 = get_month_and_gamecounter(request)
    
    for obj in games:
        obj.winner = winnerpool.get(obj.winner)
        obj.r1 = rolepool.get(obj.r1)
        obj.r2 = rolepool.get(obj.r2)
        obj.r3 = rolepool.get(obj.r3)
        obj.r4 = rolepool.get(obj.r4)
        obj.r5 = rolepool.get(obj.r5)
        obj.r6 = rolepool.get(obj.r6)
        obj.r7 = rolepool.get(obj.r7)
        obj.r8 = rolepool.get(obj.r8)
        obj.r9 = rolepool.get(obj.r9)
        obj.r10 = rolepool.get(obj.r10)

        for i in range(1, 11):
            attr_name = f'd{i}'
            value = getattr(obj, attr_name)
            if value == 0.0:
                setattr(obj, attr_name, '-')
            else:
                setattr(obj, attr_name, f'{"+" if value > 0 else "-"}{abs(value)}')
                
        if obj.p_lh == 0:
            obj.p_lh = "Нет"
        else:
            values = [obj.p1, obj.p2, obj.p3, obj.p4, obj.p5, obj.p6, obj.p7, obj.p8, obj.p9, obj.p10]
            obj.p_lh = values[obj.p_lh - 1]

        lh_counter = 0
        lh_redcounter = 0
        roles = ['Мафия', 'Дон', 'Мирный', 'Шериф']
        for i in range(1, 4):
            for j in range(1, 11):
                if getattr(obj, f'lh{i}') == j and getattr(obj, f'r{j}') in roles[:2]:
                    lh_counter += 1
                elif getattr(obj, f'lh{i}') == j and getattr(obj, f'r{j}') in roles[2:]:
                    lh_redcounter += 1

        obj.bestmove = '-'
        if lh_redcounter == 3:
            obj.bestmove = '3 красных'
        if lh_counter == 1:
            obj.bestmove = '1 черного'
        if lh_counter == 2:
            obj.bestmove = '2 черных'
        if lh_counter == 3:
            obj.bestmove = '3 черных'
    
    return games

#Отображение главной страницы
def index(request):
    month, gamecounter, season, currectyear, currectmonth, fullseason, month1, month2, month3 = get_month_and_gamecounter(request)
    if request.method == 'POST':
        if request.POST.get('type') == 'season':
            table = list(Raiting.objects.filter(seasonmonth=month1, seasonyear=currectyear))
            table2 = list(Raiting.objects.filter(seasonmonth=month2, seasonyear=currectyear))
            table3 = list(Raiting.objects.filter(seasonmonth=month3, seasonyear=currectyear))
        #Сделать слияние трех таблиц посредством двойного цикла 
        #проходящего по всем записям и ищущего совпадения ником. 
        # В нем суммируются основные поля. Потом отдельно присходит 
        # перерассчет вычисляемых полей
        
        # Добавляем игроков из table2, которых нет в table
            for old in table2:
                found_in_table = False
                for new in table:
                    if old.nick == new.nick:
                        found_in_table = True
                        break
                if not found_in_table:
                    table.append(old)

            # Добавляем игроков из table3, которых нет в table
            for old3 in table3:
                found_in_table = False
                for new in table:
                    if old3.nick == new.nick:
                        found_in_table = True
                        break
                if not found_in_table:
                    table.append(old3)
                    
            for new in table:
                found_in_table2 = False
                for old in table2:
                    if new.nick == old.nick:
                        new.donwin += old.donwin
                        new.donloose += old.donloose
                        new.sherifwin += old.sherifwin
                        new.sherifloose += old.sherifloose
                        new.mirwin += old.mirwin
                        new.mirloose += old.mirloose
                        new.mafwin += old.mafwin
                        new.mafloose += old.mafloose
                        new.nowinner += old.nowinner
                        new.dop += old.dop
                        new.compens += old.compens
                        new.straf += old.straf
                        new.twomaf += old.twomaf
                        new.threemaf += old.threemaf
                        new.threered += old.threered
                        new.total_win += old.total_win
                        new.total_loose += old.total_loose
                        new.total_game += old.total_game
                        new.losses += old.losses
                        found_in_table2 = True

                for old3 in table3:
                    if new.nick == old3.nick:
                        new.donwin += old3.donwin
                        new.donloose += old3.donloose
                        new.sherifwin += old3.sherifwin
                        new.sherifloose += old3.sherifloose
                        new.mirwin += old3.mirwin
                        new.mirloose += old3.mirloose
                        new.mafwin += old3.mafwin
                        new.mafloose += old3.mafloose
                        new.nowinner += old3.nowinner
                        new.dop += old3.dop
                        new.compens += old3.compens
                        new.straf += old3.straf
                        new.twomaf += old3.twomaf
                        new.threemaf += old3.threemaf
                        new.threered += old3.threered
                        new.total_win += old3.total_win
                        new.total_loose += old3.total_loose
                        new.total_game += old3.total_game
                        new.losses += old3.losses
            
            for obj in table:
                obj.total_win = obj.donwin + obj.mafwin + obj.sherifwin + obj.mirwin
                obj.total_loose = obj.donloose + obj.mafloose + obj.sherifloose + obj.mirloose + obj.nowinner
                obj.total_game = obj.total_loose + obj.total_win
                obj.losses = obj.total_loose - obj.nowinner
                if obj.total_loose == 0:
                    obj.winrate = 100
                else:
                    obj.winrate = round(((obj.total_win / obj.total_game) * 100))
                obj.ball = round(((obj.mirwin * 2) + (obj.sherifwin * 2) + (obj.donwin * 2) + (obj.mafwin * 2) 
                                + obj.dop + obj.straf + (obj.compens * 0.25) + (obj.twomaf * 0.25) + (obj.threemaf * 0.4) - (obj.threered * 0.25)),2)
                obj.med_ball = round((obj.ball / obj.total_game),2)
                obj.itog = round ((((obj.ball * obj.winrate) / 100) * obj.med_ball),2)              
            
            table.sort(key=lambda x: x.itog, reverse=True)
        else:
            table = Raiting.objects.all().filter(seasonmonth=currectmonth, seasonyear=currectyear).order_by('-itog')
    else:
        table = Raiting.objects.all().filter(seasonmonth=currectmonth, seasonyear=currectyear).order_by('-itog')
    if '_' in request.user.username:
        request.user.username = request.user.username.replace('_', ' ')
    return render(request, 'index.html', {'title': 'Temnota Mafia Club - Сводный рейтинг', 'table': table, 'month': month, 
                                          'currectyear':currectyear, 'gamecounter': gamecounter,
                                          'season':season, 'fullseason':fullseason})

#Отображение лейбла успешного внесения игр и возвращение на страницу внесения игр
@staff_only #Отправляет на def staff_check для проверки статуса персонала и далее по логике staff_only и access_denied_view
def gamead(request):
    outputlabel = 'Игра успешно внесена'
    season = Season.objects.all()
    return render (request, 'game.html', {'title': 'Внесение игр', 'outputlabel': outputlabel, 'season':season})

#Отображение страницы внесения игры и её внесение в случае method=post
@staff_only
def game(request):
    if request.method == 'POST':
        p_list = [request.POST.get(f'p{i}') for i in range(1, 11)]
        r_list = [request.POST.get(f'r{i}') for i in range(1, 11)]
        d_list = [float(request.POST.get(f'd{i}')) for i in range(1, 11)]

        game_data = {
            'p1': p_list[0],
            'p2': p_list[1],
            'p3': p_list[2],
            'p4': p_list[3],
            'p5': p_list[4],
            'p6': p_list[5],
            'p7': p_list[6],
            'p8': p_list[7],
            'p9': p_list[8],
            'p10': p_list[9],
        
            'r1': r_list[0],
            'r2': r_list[1],
            'r3': r_list[2],
            'r4': r_list[3],
            'r5': r_list[4],
            'r6': r_list[5],
            'r7': r_list[6],
            'r8': r_list[7],
            'r9': r_list[8],
            'r10': r_list[9],
                    
            'd1': d_list[0],
            'd2': d_list[1],
            'd3': d_list[2],
            'd4': d_list[3],
            'd5': d_list[4],
            'd6': d_list[5],
            'd7': d_list[6],
            'd8': d_list[7],
            'd9': d_list[8],
            'd10': d_list[9],
                    
            'p_lh': request.POST.get('p_lh'),
            'lh1': request.POST.get('lh1'),
            'lh2': request.POST.get('lh2'),
            'lh3': request.POST.get('lh3'),
            'gamedate': request.POST.get('gamedate'),
            'regdate': datetime.now(),
            'winner': request.POST.get('winner'),
        }

        Game.objects.create(**game_data)
        return redirect('gamead')
    else:
        season = Season.objects.all().order_by('-date')
        return render (request, 'game.html', {'title': 'Внесение игр', 'season':season})

#Отображение страницы админ панели  
@staff_only
def adminpanel(request):
    username = request.user.username
    return render (request, 'adminpanel.html', {'title': 'Админ панель', 'username':username}) 

#Отображение страницы игроков на админ панели. Если method=post то добавление пользователя по нику из формы
@staff_only
def player(request):
    if request.method == 'POST':
        if Player.objects.filter(name=request.POST.get('name'),).exists():
            return redirect('playerhas')
        else:
            Player.objects.create(
                name=request.POST.get('name'),
            )
            return redirect('playerad')
    else:
        players = Player.objects.all().order_by('name')
        return render (request, 'player.html', {'title': 'Игроки', 'players':players})

#Создание лейбла об успешном добавлении игрока и возвращение на страницу player
@staff_only
def playerad(request):
    outputlabel = "Игрок внесён успешно"
    players = Player.objects.all()
    return render (request, 'player.html', {'title': 'Игроки', 'players':players, 'outputlabel':outputlabel})

#Создание лейбла о том что игрок уже есть в бд
@staff_only
def playerhas(request):
    outputlabel = "Игрок уже есть в базе"
    players = Player.objects.all()
    return render (request, 'player.html', {'title': 'Игроки', 'players':players, 'outputlabel':outputlabel})

#ajax для дописывания ников игроков
def player_autocomplete(request):
    query = request.GET.get('q')
    if query:
        players = Player.objects.filter(name__icontains=query)
        results = [{'id': player.id, 'label': player.name, 'value': player.name} for player in players]
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse([], safe=False)

#функция обновления статистики для ничьей
def update_player_nowinner(nick, gamedate):
    if Raiting.objects.filter(nick=nick).exists():
        player = Raiting.objects.get(nick=nick)
    else:
        # Создание записи в бд и увеличение счетчика если игрока ещё нет в таблице
        Raiting.objects.create(
            nick=nick,
            donwin=0,
            donloose=0,
            sherifwin=0,
            sherifloose=0,
            mirwin=0,
            mirloose=0,
            mafwin=0,
            mafloose=0,
            dop=0,
            compens=0,
            straf=0,
            twomaf=0,
            threemaf=0, 
            threered=0,
            nowinner=0,
            seasonmonth = gamedate.month,
            seasonyear = gamedate.year
        )
        player = Raiting.objects.get(nick=nick)
        player.nowinner = player.nowinner + 1
        player.save(update_fields=["nowinner"])

#Высчитыванние счетчиков побед, лх, ролей для игроков по всем играм     
def update_player_stats(obj, raitings: QuerySet, idcount: int, player_stats: Dict[Tuple[str, str], Tuple[str, int]]) -> None:
    for i in range(1, 11):
        player_name = getattr(obj, f"p{i}")
            
        if player_name:
            try:
                # Получение всех строк сезонов, соответствующих игроку
                player_seasons = Raiting.objects.filter(nick=player_name, seasonmonth=obj.gamedate.month, seasonyear=obj.gamedate.year)
                # Если игрок не найден для текущего сезона, создаем новую строку для него
                if not player_seasons.exists():
                    player = Raiting.objects.create(
                        id=idcount,
                        nick=player_name,
                        donwin=0,
                        donloose=0,
                        sherifwin=0,
                        sherifloose=0,
                        mirwin=0,
                        mirloose=0,
                        mafwin=0,
                        mafloose=0,
                        dop=0,
                        compens=0,
                        straf=0,
                        twomaf=0,
                        threemaf=0,
                        threered=0,
                        nowinner=0,
                        seasonmonth=obj.gamedate.month,
                        seasonyear=obj.gamedate.year,
                    )
                    idcount += 1
                else:
                    player = player_seasons.first()

                # Добавка текущей роли в таблицу
                attr, value = player_stats.get((getattr(obj, f"r{i}"), obj.winner), (None, 0))
                if attr is not None:
                    setattr(player, attr, getattr(player, attr) + value)

                # Допы
                if getattr(obj, f"d{i}") > 0:
                    player.dop += getattr(obj, f"d{i}")
                else:
                    player.straf += getattr(obj, f"d{i}")

                # Лучший ход    
                if getattr(obj, f"p_lh") == i:
                    lh_counter = 0
                    lh_redcounter = 0
                    for lh in range(1, 4):
                        for r in range(1, 11):
                            if getattr(obj, f"lh{lh}") == r and getattr(obj, f"r{r}") in ["maf", "don"]:
                                lh_counter += 1
                            elif getattr(obj, f"lh{lh}") == r and getattr(obj, f"r{r}") == "mir":
                                lh_redcounter += 1
                    # обновление счетчиков лх в таблице
                    if lh_redcounter == 3:
                        player.threered += 1
                    if lh_counter == 2:
                        player.twomaf += 1
                    if lh_counter == 3:
                        player.threemaf += 1
                    # проверка компенсации
                    if getattr(obj, f"p_lh") == i and (getattr(obj, f"r{i}") == "mir" or getattr(obj, f"r{i}") == "ser") and obj.winner == "maf":
                        player.compens += 1
                
                player.save(update_fields=["seasonmonth", "seasonyear", "donwin","donloose","sherifwin","sherifloose","mirwin","mirloose","mafwin","mafloose","dop","compens","straf","twomaf","threemaf","threered"])
            except Exception as e:
                print(f"An error occurred: {e}")

#Высчитыванние статистики игроков по всем играм сезона
def update_raiting_stats_withseason(currectmonth, currectyear):
    objects = Raiting.objects.all()
    for obj in objects:
        if obj.seasonmonth == currectmonth and obj.seasonyear == currectyear:
            obj.total_win = obj.donwin + obj.mafwin + obj.sherifwin + obj.mirwin
            obj.total_loose = obj.donloose + obj.mafloose + obj.sherifloose + obj.mirloose + obj.nowinner
            obj.total_game = obj.total_loose + obj.total_win
            obj.losses = obj.total_loose - obj.nowinner
            if obj.total_loose == 0:
                obj.winrate = 100
            else:
                obj.winrate = round(((obj.total_win / obj.total_game) * 100))
            obj.ball = round(((obj.mirwin * 2) + (obj.sherifwin * 2) + (obj.donwin * 2) + (obj.mafwin * 2) 
                            + obj.dop + obj.straf + (obj.compens * 0.25) + (obj.twomaf * 0.25) + (obj.threemaf * 0.4) - (obj.threered * 0.25)),2)
            obj.med_ball = round((obj.ball / obj.total_game),2)
            obj.itog = round ((((obj.ball * obj.winrate) / 100) * obj.med_ball),2)
            obj.save(update_fields=["total_win", "total_loose", "losses", "total_game", "winrate", "ball", "med_ball", "itog"])
 
#Общая функция перерассчета рейтинга                       
def raitingcalculate(request):
    player_stats = {
    ('mir', 'mir'): ('mirwin', 1),
    ('mir', 'maf'): ('mirloose', 1),
    ('ser', 'mir'): ('sherifwin', 1),
    ('ser', 'maf'): ('sherifloose', 1),
    ('maf', 'maf'): ('mafwin', 1),
    ('maf', 'mir'): ('mafloose', 1),
    ('don', 'maf'): ('donwin', 1),
    ('don', 'mir'): ('donloose', 1)
    }

    season = Season.objects.filter(id=request.POST.get('selected_option')).get()
    currectmonth = season.date.month
    currectyear = season.date.year
    idcount=1
    
    Raiting.objects.all().filter(seasonmonth=currectmonth, seasonyear=currectyear).delete()
    
    # Если игрок найден для других сезонов, нужно отдельно внести первую игру (костыль)
    if Raiting.objects.exists():
        my_object = Game.objects.filter(gamedate__month=currectmonth, gamedate__year=currectyear).earliest('gamedate')
        firstobject = Game.objects.order_by('id').first()
        if firstobject.gamedate.month == currectmonth and firstobject.gamedate.year == currectyear:
            skip=1
        else:
            update_player_stats(my_object, Raiting.objects.all(), idcount, player_stats)
            max_id = Raiting.objects.aggregate(Max('id'))['id__max']
            idcount = max_id + 1 if max_id is not None else 1
    else:
        idcount = 1
    
    my_objects = Game.objects.all().filter(gamedate__month=currectmonth, gamedate__year=currectyear)    
    for obj in my_objects:
        if obj.winner == "not":
            update_player_nowinner(obj.p1, obj.gamedate)
            update_player_nowinner(obj.p2, obj.gamedate)
            update_player_nowinner(obj.p3, obj.gamedate)
            update_player_nowinner(obj.p4, obj.gamedate)
            update_player_nowinner(obj.p5, obj.gamedate)
            update_player_nowinner(obj.p6, obj.gamedate)
            update_player_nowinner(obj.p7, obj.gamedate)
            update_player_nowinner(obj.p8, obj.gamedate)
            update_player_nowinner(obj.p9, obj.gamedate)
            update_player_nowinner(obj.p10, obj.gamedate)
        else:
            update_player_stats(obj, Raiting.objects.all(), idcount, player_stats)
            idcount = Raiting.objects.aggregate(Max('id'))['id__max'] + 1
    update_raiting_stats_withseason(currectmonth, currectyear)
    
    return redirect('admingameslist')

#Спискок игр на админке
@staff_only
def admingameslist(request):
    month, gamecounter, season, currectyear, currectmonth, fullseason, month1, month2, month3 = get_month_and_gamecounter(request)
    games = Game.objects.all().filter(gamedate__month=currectmonth, gamedate__year=currectyear).order_by('-gamedate')
    if request.method == 'POST':
        if request.POST.get('date') != "":
            games = Game.objects.all().filter(gamedate=request.POST.get('date'))
    games = games_selector(request, games)
    gamecounter = games.count
    if request.method == 'POST':
        if request.POST.get('date') != "":
            if games.exists():                
                month = games.first()
                month = month.gamedate
            else:
                month = request.POST.get('date')
            currectyear = ""
    return render(request, 'admingameslist.html', {'title': 'Список игр', 'month': month, 'currectyear':currectyear, 
                                             'gamecounter': gamecounter,'season':season, 'games':games})

#Редактирование игр на админке
@staff_only 
def admingamesedit(request):
    if request.method == 'POST':
        gameid = request.POST.get('id')
        game = Game.objects.get(id=gameid)
        return render(request, 'gamesedit.html', {'title': 'Внесение игр', 'game':game, 'gameid':gameid})
    else:
        return redirect('admingameslist')
                  

#Удаление игр на админке
@staff_only
def admingamesdelete(request):
    id = request.POST.get('id')
    Game.objects.get(id=id).delete()
    return redirect('admingameslist')

#Спискок игр для всех игроков
def gameslist(request):
    month, gamecounter, season, currectyear, currectmonth, fullseason, month1, month2, month3 = get_month_and_gamecounter(request)
    games = Game.objects.all().filter(gamedate__month=currectmonth, gamedate__year=currectyear).order_by('-gamedate')
    if request.method == 'POST':
        if request.POST.get('date') != "":
            games = Game.objects.all().filter(gamedate=request.POST.get('date'))
    games = games_selector(request, games)
    gamecounter = games.count
    if request.method == 'POST':
        if request.POST.get('date') != "":
            if games.exists():                
                month = games.first()
                month = month.gamedate
            else:
                month = request.POST.get('date')
            currectyear = ""
    return render(request, 'gameslist.html', {'title': 'Список игр', 'month': month, 'currectyear':currectyear, 
                                             'gamecounter': gamecounter,'season':season, 'games':games})

#Высчитыванние статистики игроков по всем играм
@login_required
def profile(request):
    month, gamecounter, season, currectyear, currectmonth, fullseason, month1, month2, month3 = get_month_and_gamecounter(request)
    games = Game.objects.all().filter(gamedate__month=currectmonth, gamedate__year=currectyear).order_by('-gamedate')
    if request.method == 'POST':
        if request.POST.get('date') != "":
            games = Game.objects.all().filter(gamedate=request.POST.get('date'))
    if '_' in request.user.username:
        request.user.username = request.user.username.replace('_', ' ')
    games = games.filter(Q(p1=request.user.username) | Q(p2=request.user.username) | Q(p3=request.user.username) | Q(p4=request.user.username) 
                             | Q(p5=request.user.username) | Q(p6=request.user.username) | Q(p7=request.user.username) | Q(p8=request.user.username) 
                             | Q(p9=request.user.username) | Q(p10=request.user.username)).all()
    gamecounter = games.count
    games = games_selector(request, games)
    if request.method == 'POST':
        if request.POST.get('date') != "":
            if games.exists():                
                month = games.first()
                month = month.gamedate
            else:
                month = request.POST.get('date')
            currectyear = ""
    return render(request, 'users/profile.html', {'title': 'Профиль', 'month': month, 'currectyear':currectyear, 
                                             'gamecounter': gamecounter,'season':season, 'games':games})
    
@login_required
def admingameseditsave(request):
    if request.method == 'POST':
        p_list = [request.POST.get(f'p{i}') for i in range(1, 11)]
        r_list = [request.POST.get(f'r{i}') for i in range(1, 11)]
        d_list = [float(request.POST.get(f'd{i}').replace(',', '.')) for i in range(1, 11)]
        game_data = {
            'p1': p_list[0],
            'p2': p_list[1],
            'p3': p_list[2],
            'p4': p_list[3],
            'p5': p_list[4],
            'p6': p_list[5],
            'p7': p_list[6],
            'p8': p_list[7],
            'p9': p_list[8],
            'p10': p_list[9],
        
            'r1': r_list[0],
            'r2': r_list[1],
            'r3': r_list[2],
            'r4': r_list[3],
            'r5': r_list[4],
            'r6': r_list[5],
            'r7': r_list[6],
            'r8': r_list[7],
            'r9': r_list[8],
            'r10': r_list[9],
                    
            'd1': d_list[0],
            'd2': d_list[1],
            'd3': d_list[2],
            'd4': d_list[3],
            'd5': d_list[4],
            'd6': d_list[5],
            'd7': d_list[6],
            'd8': d_list[7],
            'd9': d_list[8],
            'd10': d_list[9],
                    
            'p_lh': request.POST.get('p_lh'),
            'lh1': request.POST.get('lh1'),
            'lh2': request.POST.get('lh2'),
            'lh3': request.POST.get('lh3'),
            'regdate': datetime.now(),
            'winner': request.POST.get('winner'),
        }
        gameid = request.POST.get('id')
        Game.objects.filter(id=gameid).update(**game_data)
        game = Game.objects.get(id=gameid)
        outputlabel = "Изменения сохранены"
        return render(request, 'gamesedit.html', {'title': 'Редактирование', 'outputlabel': outputlabel, 'gameid':gameid, 'game':game})
    else:
        return redirect('admingameslist')
