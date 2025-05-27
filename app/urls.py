from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
   path('voltar/<str:onde>', funcaoIntermediariaVoltar, name='voltar'),
   path('criarProva/', criarProva, name='criarProva'),  
   path('listarProvas/', listarProvas, name='listarProvas'), 
   path('corrigirProva/<str:id>', corrigirProva, name='corrigirProva'),
   path('adicionaBancoDeDados/<str:adicionaOQue>/<str:idProva>', adicionaBancoDeDados, name='adicionaBancoDeDados'),
   path('modificaDados/<str:acao>/<str:modelName>/<str:id>', modificaDados, name='modificaDados'),
   path('redirecionaDetalhes/<int:provaId>', redirecionaDetalhes, name='redirecionaDetalhes' ),
   path('definirTempo/', DefineTimeDescription.as_view(), name='definirTempo' )
   
]
