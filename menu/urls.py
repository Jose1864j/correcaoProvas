from django.contrib import admin
from django.urls import path,include
from  .views import start, redirectStart, selecionar

urlpatterns = [
   path('', redirectStart),
   path('iniciar/', start, name='start'),
   path('selecionar/<path:url>', selecionar, name='selecionar')

]
