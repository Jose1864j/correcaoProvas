from django.shortcuts import render
from app.models import *
from django.http import HttpResponse
from config.funcoes import *
import re
def carregaDetalhes(request, provaId):
    filtrarPor = True
    if request.method == 'POST':
        opcao = request.POST.get('filtrarAcertosErros')
        filtrarPor = eval(opcao)

    prova  = Prova.objects.get(id=provaId)
    materias = Materia.objects.all()
    questoesTotais = Questoes.objects.filter(prova=prova)
    qntQuestoesTotais = []
    qntQuestoesPorMateria = {}
    tipos = {True: ['certeza', 'duvida', 'chute'], False: ['conteudo', 'atencao', 'tempo']}
    
    for tipo in tipos[filtrarPor]:
        qntQuestoesTotais.append(colocaZeroAntes(fazBuscaQuestoes(prova,filtrarPor,tipo,'all').count()))
    qntQuestoesTotais.append(f'{colocaZeroAntes(fazBuscaQuestoes(prova,filtrarPor,'all','all').count())}/{colocaZeroAntes(questoesTotais.count())}')
    if questoesTotais.count() == 0:
        qntQuestoesTotais.append(f'0.00%')

    else:
        qntQuestoesTotais.append(f'{fazBuscaQuestoes(prova,'all','all','all').count()/questoesTotais.count()  *100}%')

    

    for materia in materias:
        if materia.nome not in qntQuestoesPorMateria:
            qntQuestoesPorMateria[materia.nome] = []
        for tipo in tipos[filtrarPor]:

            qntQuestoesPorMateria[materia.nome].append(colocaZeroAntes(fazBuscaQuestoes(prova,filtrarPor,tipo,materia).count()))
        totalPorStatus = colocaZeroAntes(fazBuscaQuestoes(prova, filtrarPor, 'all', materia=materia).count())

        
        porcentagem = f'{int(totalPorStatus) / fazBuscaQuestoes(prova,status='all', tipo='all', materia=materia).count()  * 100:.2f}%' if int(totalPorStatus) != 0 else f'0%'
        qntQuestoesPorMateria[materia.nome].append(totalPorStatus)
        qntQuestoesPorMateria[materia.nome].append(porcentagem)
        
   
    #código do gpt para ordenar o idcionario de acodo com a porcentagem
    qn = dict(
        sorted(
        qntQuestoesPorMateria.items(),
        key=lambda item: float(item[1][-1].strip('%')),  # Converte '12.50%' para 12.50
        reverse=True  # Ordem decrescente
    )
)
    return render(request, 'viewDetails.html', {'prova':prova,'qntQuestoesPorMateria': qn,'filtrarPor':filtrarPor, 'qntQuestoesTotais':qntQuestoesTotais})



def detalhesTotal(request):


    detalhaOque = 'Vocabulario'
    modelsPertence = 'Vocabulario'
    valores = Vocabulario.objects.all()
    if request.method == 'POST':
        selecionado = request.POST.get('selecionarConteudo')
        if selecionado == 'ConteudoRever':
            detalhaOque = 'Conteudo rever'
            valores = ConteudoRever.objects.all()
        elif selecionado == 'ConteudoPrecisoVer':
            valores = ConteudoPrecisoVer.objects.all()
            detalhaOque = 'Conteudos preciso ver'

        modelsPertence = selecionado
      

    return render(request, 'listarConteudos.html', {'detalhaOQue':detalhaOque, 'modelsPertence':modelsPertence, 'valores':valores})