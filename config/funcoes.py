from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from app.models import *
def printDict(dictionary):
    if not isinstance(dictionary, dict):
        print("O valor fornecido não é um dicionário.")
        return
    
    # Iterando sobre o dicionário e imprimindo chave-valor de forma legível
    for key, value in dictionary.items():
        print(f'{key}: {value}')

            
          
def irPara(onde):
    if onde == 'menu':
        return redirect('/menu/iniciar/')
    elif onde ==  'listarProvas': 
        return redirect('/prova/listarProvas/')
    return HttpResponse('Não feito ainda ')
                

def fazBuscaQuestoes(prova,status,tipo, materia):
    
    if status == 'all':
        if tipo == 'all' and materia == 'all':
            return Questoes.objects.filter(prova=prova) 

        elif tipo == 'all':
            return Questoes.objects.filter(prova=prova, materia=materia)

        


    elif tipo == 'all':
        if materia == 'all':
            
            return Questoes.objects.filter(prova=prova, acertou=status) 
    
        return Questoes.objects.filter(prova=prova,materia=materia, acertou=status)

    elif status == True:
        if materia == 'all':
            return Questoes.objects.filter(prova=prova,tipoAcerto=tipo, acertou=status)
        
        return Questoes.objects.filter(prova=prova,tipoAcerto=tipo, materia=materia, acertou=status)
 
    elif status== False:
        if materia == 'all':
            return Questoes.objects.filter(prova=prova,tipoErro=tipo, acertou=status)
        
        return Questoes.objects.filter(prova=prova,tipoErro=tipo, materia=materia, acertou=status)

    



def colocaZeroAntes(numero):
    isFloat = False
    try: 
        numero = int(numero)

    except:
        numero = float(numero)
        isFloat = True
    if numero <= 9 and numero >=-9:
       
        return '0' + str(numero)
    return numero
