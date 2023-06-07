from django.db import models
from datetime import datetime

# Create your models here.
    
class Raiting(models.Model):
    id = models.BigAutoField(primary_key=True)
    nick = models.CharField(max_length=100, verbose_name="Никнейм")
    donwin = models.IntegerField(verbose_name="Дон (вин)")
    donloose = models.IntegerField(verbose_name="Дон (луз)")
    sherifwin = models.IntegerField(verbose_name="Шер (вин)")
    sherifloose = models.IntegerField(verbose_name="Шер (луз)")
    mirwin = models.IntegerField(verbose_name="Мир (вин)")
    mirloose = models.IntegerField(verbose_name="Мир (луз)")
    mafwin = models.IntegerField(verbose_name="Маф (вин)")
    mafloose = models.IntegerField(verbose_name="Маф (луз)")
    nowinner = models.IntegerField(verbose_name="Ничья")
    dop = models.FloatField(verbose_name="Доп")
    compens = models.IntegerField(verbose_name="Компенсация")
    straf = models.FloatField(verbose_name="Штраф")
    twomaf = models.IntegerField(verbose_name="2 черных")
    threemaf = models.IntegerField(verbose_name="3 черных")
    threered = models.IntegerField(verbose_name="3 красных")
    total_win = models.IntegerField(verbose_name="Всего побед", default=0)
    total_loose = models.IntegerField(verbose_name="Всего поражений", default=0)
    total_game = models.IntegerField(verbose_name="Всего игр", default=0)
    losses = models.IntegerField(verbose_name="Лузы", default=0)
    winrate = models.IntegerField(verbose_name="% побед", default=0)
    ball = models.FloatField(verbose_name="Баллы", default=0)
    med_ball = models.FloatField(verbose_name="Средний балл", default=0)
    itog = models.FloatField(verbose_name="Средний балл", default=0)
    seasonmonth = models.IntegerField(verbose_name="Месяц сезона")
    seasonyear = models.IntegerField(verbose_name="Год сезона") 

class Player(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Никнейм")

class Game(models.Model):
    
    role = (
        ('maf', 'Мафия'),
        ('don', 'Дон'),
        ('ser', 'Шериф'),
        ('mir', 'Мирный'),
    )
    lh = (
        (0,'-'),
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        (6,'6'),
        (7,'7'),
        (8,'8'),
        (9,'9'),
        (10,'10'),
    )
    win = (
        ('maf','Мафия'),
        ('mir','Мирные'),
        ('not','Ничья'),
    )
    
    gamedate = models.DateField(verbose_name="Дата игры", default=datetime.now(tz=None))
    regdate = models.DateField(verbose_name="Дата внесения", default=datetime.now(tz=None))
    p1 = models.CharField(max_length=100, verbose_name="Никнейм 1")
    p2 = models.CharField(max_length=100, verbose_name="Никнейм 2")
    p3 = models.CharField(max_length=100, verbose_name="Никнейм 3")
    p4 = models.CharField(max_length=100, verbose_name="Никнейм 4")
    p5 = models.CharField(max_length=100, verbose_name="Никнейм 5")
    p6 = models.CharField(max_length=100, verbose_name="Никнейм 6")
    p7 = models.CharField(max_length=100, verbose_name="Никнейм 7")
    p8 = models.CharField(max_length=100, verbose_name="Никнейм 8")
    p9 = models.CharField(max_length=100, verbose_name="Никнейм 9")
    p10 = models.CharField(max_length=100, verbose_name="Никнейм 10")
    r1 = models.CharField(max_length=3, choices=role, default='mir', verbose_name="Роль игрока 1")
    r2 = models.CharField(max_length=3, choices=role, default='mir', verbose_name="Роль игрока 2")
    r3 = models.CharField(max_length=3, choices=role, default='mir', verbose_name="Роль игрока 3")
    r4 = models.CharField(max_length=3, choices=role, default='mir', verbose_name="Роль игрока 4")
    r5 = models.CharField(max_length=3, choices=role, default='mir', verbose_name="Роль игрока 5")
    r6 = models.CharField(max_length=3, choices=role, default='mir', verbose_name="Роль игрока 6")
    r7 = models.CharField(max_length=3, choices=role, default='mir', verbose_name="Роль игрока 7")
    r8 = models.CharField(max_length=3, choices=role, default='mir', verbose_name="Роль игрока 8")
    r9 = models.CharField(max_length=3, choices=role, default='mir', verbose_name="Роль игрока 9")
    r10 = models.CharField(max_length=3, choices=role, default='mir', verbose_name="Роль игрока 10")
    d1 = models.FloatField(verbose_name="Доп игрока 1", default=0)
    d2 = models.FloatField(verbose_name="Доп игрока 2", default=0)
    d3 = models.FloatField(verbose_name="Доп игрока 3", default=0)
    d4 = models.FloatField(verbose_name="Доп игрока 4", default=0)
    d5 = models.FloatField(verbose_name="Доп игрока 5", default=0)
    d6 = models.FloatField(verbose_name="Доп игрока 6", default=0)
    d7 = models.FloatField(verbose_name="Доп игрока 7", default=0)
    d8 = models.FloatField(verbose_name="Доп игрока 8", default=0)
    d9 = models.FloatField(verbose_name="Доп игрока 9", default=0)
    d10 = models.FloatField(verbose_name="Доп игрока 10", default=0)
    p_lh = models.IntegerField(choices=lh, verbose_name="Первоубиенный игрок (номер)", default=0)
    lh1 = models.IntegerField(choices=lh, verbose_name="ЛХ 1", default=0)
    lh2 = models.IntegerField(choices=lh, verbose_name="ЛХ 2", default=0)
    lh3 = models.IntegerField(choices=lh, verbose_name="ЛХ 3", default=0)
    winner = models.CharField(max_length=3, choices=win, verbose_name="Победившая команда", default='mir')
    
class Season(models.Model):
    id = models.BigAutoField(primary_key=True)
    month = models.CharField(max_length=20, verbose_name="Месяц")
    year = models.IntegerField(verbose_name="Год", default=0)
    date = models.DateField(verbose_name="Начало сезона в числовом формате", default='Null')
    
class FullSeason(models.Model):
    id = models.BigAutoField(primary_key=True)
    season = models.CharField(max_length=20, verbose_name="Название сезона")
    year = models.IntegerField(verbose_name="Год", default=0)
    date1 = models.DateField(verbose_name="Начало первого месяца в числовом формате", default='Null')
    date2 = models.DateField(verbose_name="Начало второго месяца в числовом формате", default='Null')
    date3 = models.DateField(verbose_name="Начало третьего месяца в числовом формате", default='Null')
