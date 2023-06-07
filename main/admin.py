from django.contrib import admin
from .models import Raiting, Game, Player, Season, FullSeason
# Register your models here.
    
class MyRaitingAdmin(admin.ModelAdmin):
    # list_display controls which fields are displayed in the list view of the model in the admin panel
    list_display = ('id', 'nick', 'itog', 'seasonmonth', 'seasonyear', 'ball', 'total_game', 'winrate', 'med_ball', 'total_win', 'total_loose', 'nowinner', 'sherifwin', 'sherifloose', 
                    'mirwin', 'mirloose','donwin', 'donloose', 'mafwin', 'mafloose', 'dop', 'straf', 'compens', 'twomaf', 'threemaf', 'threered')

admin.site.register(Raiting, MyRaitingAdmin)

class MyPlayerAdmin(admin.ModelAdmin):
    # list_display controls which fields are displayed in the list view of the model in the admin panel
    list_display = ('id', 'name')

admin.site.register(Player, MyPlayerAdmin)

class MyGameAdmin(admin.ModelAdmin):
    # list_display controls which fields are displayed in the list view of the model in the admin panel
    list_display = ('id', 'regdate', 'gamedate','p1','p2','p3','p4','p5',
                    'p6','p7','p8','p9','p10',
                    'r1','r2','r3','r4','r5','r6','r7','r8','r9','r10',
                    'd1','d2','d3','d4','d5','d6','d7','d8','d9','d10',
                    'p_lh','lh1','lh2','lh3','winner')

admin.site.register(Game, MyGameAdmin)

class MySeasonAdmin(admin.ModelAdmin):
    # list_display controls which fields are displayed in the list view of the model in the admin panel
    list_display = ('id', 'month', 'year', 'date')

admin.site.register(Season, MySeasonAdmin)

class MyFullSeasonAdmin(admin.ModelAdmin):
    # list_display controls which fields are displayed in the list view of the model in the admin panel
    list_display = ('id', 'season', 'year', 'date1', 'date2', 'date3')

admin.site.register(FullSeason, MyFullSeasonAdmin)