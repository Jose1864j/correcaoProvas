from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('detalhesProva/<int:provaId>', carregaDetalhes, name='carregaDetalhes' ),
    path('detalhesTotal/', detalhesTotal, name='detalhesTotal'),
    

]