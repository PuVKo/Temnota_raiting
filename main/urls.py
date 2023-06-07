"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .views import player_autocomplete

urlpatterns = [
    path ('', views.index, name='index'),
    path ('gameslist', views.gameslist, name='gameslist'),
    path ('profile', views.profile, name='profile'),
    
    path ('adminpanel', views.adminpanel, name='adminpanel'),
    
    path ('game', views.game, name='game'),
    path ('gamead', views.gamead, name='gamead'),
    

        
    path ('raitingcalculate', views.raitingcalculate, name='raitingcalculate'),
    
    path ('player', views.player, name='player'),
    path ('playerad', views.playerad, name='playerad'),
    path ('playerhas', views.playerhas, name='playerhas'),
    
    path ('admingameslist', views.admingameslist, name='admingameslist'),
    path ('admingamesedit', views.admingamesedit, name='admingamesedit'),
    path ('admingameseditsave', views.admingameseditsave, name='admingameseditsave'),
    path ('admingamesdelete', views.admingamesdelete, name='admingamesdelete'),

    path('player-autocomplete/', player_autocomplete, name='player-autocomplete'),
    
    path('access_denied/', views.access_denied_view, name='access_denied'),
]
