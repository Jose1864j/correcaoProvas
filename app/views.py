from django.shortcuts import render, redirect,get_object_or_404
from django.apps import apps
from django.http import HttpResponse
from .models import Vestibular, AreasConhecimento,Materia,Prova,Questoes,StatusEnum, QuestoesErradas, Vocabulario,ConteudoPrecisoVer,ConteudoRever
from django.contrib.messages import constants
from django.contrib import messages
from config.funcoes import *
global statusProva
# Create your views here.
def funcaoIntermediariaVoltar(request, onde):
    return irPara(request, onde)
def criarProva(request):
    if request.method == 'POST':
       anoProva = request.POST.get('anoProva')
       vestibular_id = request.POST.get('vestibular')
       # Verifica se o vestibular existe e pega ele
       vestibular = get_object_or_404(Vestibular, id=vestibular_id)
       if Prova.objects.filter(ano=anoProva, vestibular=vestibular):
            messages.add_message(request, constants.SUCCESS, 'Prova já cadastrada')
            return redirect('/prova/criarProva/')
       
       prova = Prova(
           ano=anoProva,
           vestibular=vestibular
       )

       prova.save()
       return redirect('/menu/iniciar/')
    
    vestibulares  = Vestibular.objects.all()
    return render(request, 'criarProva.html', {'vestibulares': vestibulares})

def listarProvas(request):
    provas = Prova.objects.all()
    dicionarioQuantQuest = {}
    
   
    for prova in provas:
        dicionarioQuantQuest[prova.id] = colocaZeroAntes(Questoes.objects.filter(prova=prova).count())
        prova.status_value = StatusEnum[prova.status].value
  

  
        
    return render(request, 'listarProvas.html', {'provas': provas, 'dicionarioQuantQuest':dicionarioQuantQuest, "statusEnum":StatusEnum})

def corrigirProva(request, id):
    global statusProva
    
    if request.method == 'POST': 
        
        materia_id = int(request.POST.get('materiaID'))
        tipoAcerto  = request.POST.get('tipoAcertoMateria')
        tipoErro = request.POST.get('motivoErro')
        numeroQuestao = int(request.POST.get('numeroQuestao')) + 1 # +1 pq topegando a ultima questao corrigida, logo a próxima é +1 
        materia = Materia.objects.get(id=materia_id)
        letraErrou = request.POST.get('letraErrou')
        prova = Prova.objects.get(id=id)
        acertou = False
        
        
        if( tipoErro== None):
            acertou =True
            tipoErro= 'Não Errei'
        else:
            acertou = False
            tipoAcerto= 'Não acertei'

        questao =Questoes(
            prova=prova,
            acertou = acertou,
            materia=materia,
            numero=numeroQuestao,
            tipoAcerto=tipoAcerto,
            tipoErro=tipoErro
        )
        questao.save()

        if acertou == False:
            errada = QuestoesErradas(
            questao=questao,
            letraMarcada=letraErrou
            )
            errada.save()

        numeroQuestoesProva = prova.vestibular.qntQuestoes

        if numeroQuestao>= numeroQuestoesProva:
            prova.status = StatusEnum.FINALIZADO.name
            prova.save()
        elif numeroQuestao > 0:
            prova.status = StatusEnum.COMECADO.name
            prova.save()

        return redirect(f'/prova/corrigirProva/{id}')
    
    prova = Prova.objects.get(id=id)
    areasProva = prova.vestibular.areasProva.all()
    numeroQuestoes = Questoes.objects.filter(prova_id=id).count()
    materiasDaProva = []
    acertosProva = Questoes.objects.filter(prova_id=id, acertou=True)
    acertosPorMateria = {}
    qntQuestoesPorMateria = {}
    materias = {}
    questoesErradas = {}
    numeroseLetrasErradas = {}
    vocabulario = Vocabulario.objects.filter(prova=prova)
    conteudosNovos = ConteudoPrecisoVer.objects.filter(prova=prova)
    conteudosRever = ConteudoRever.objects.filter(prova=prova)

    for area in areasProva:
        materias[area] = Materia.objects.filter(areaPertence_id=area.id)
        for materia  in Materia.objects.filter(areaPertence_id=area.id):
           materiasDaProva =  materia.nome
           acertosPorMateria[materiasDaProva] = 0
           qntQuestoesPorMateria[materiasDaProva] = Questoes.objects.filter(materia_id=materia.id, prova=prova).count()
           questoesErradas[materiasDaProva] = QuestoesErradas.objects.filter(questao__prova=prova, questao__materia=materia)
        
    for chave,valores in questoesErradas.items():
        for q in valores:
            numero  = 'nada'

            if chave not in numeroseLetrasErradas:
                 numeroseLetrasErradas[chave]= set()   

            if q.questao.numero < 10:
                numero = '0' + str(q.questao.numero)

            else:  
                numero = q.questao.numero

            numeroseLetrasErradas[chave].add(f'{numero} - {q.letraMarcada}')
       
        if chave in numeroseLetrasErradas: 
            numeroseLetrasErradas[chave] =  sorted(numeroseLetrasErradas[chave])         
    
    for acerto in acertosProva:
        materia_nome = acerto.materia.nome
        if materia_nome not in acertosPorMateria:
            acertosPorMateria[materia_nome] = 0 
        acertosPorMateria[materia_nome] += 1
    
    
    qntMaxQuestoes = int(prova.vestibular.qntQuestoes)
    questoesDaProva = Questoes.objects.filter(prova=prova)
    
    return render(request, 'corrigirProva.html', {'prova': prova,'questoesDaProva':questoesDaProva, 'qntMaxQuest':qntMaxQuestoes, 'materias':materias, 'qntQuest':numeroQuestoes, "acertosPorMateria":acertosPorMateria ,"qntQuestoesPorMateria":qntQuestoesPorMateria, 'numeroseLetrasErradas':numeroseLetrasErradas, 'vocabulario':vocabulario, 'conteudosNovos':conteudosNovos, 'conteudosRever':conteudosRever})


def adicionaBancoDeDados(request, adicionaOQue, idProva):
    
    if request.method == 'POST':
        if adicionaOQue == 'novoVocabulario':
            
            nomePalavra = request.POST.get('campoPalavra')
            descricao = request.POST.get('descricaoPalavra')
            try:
                tabelaVocabulario =Vocabulario.objects.get(nome=nomePalavra)    #se não encontrar nada da erro ai vai pro except
                messages.add_message(request, constants.ERROR, 'Palavra já criada', extra_tags='vocabularioCriado')    
            except:
                if descricao == '':
                    vocabulario = Vocabulario(nome=nomePalavra,prova=Prova.objects.get(id=int(idProva)))
                    vocabulario.save() 
                else:
                    vocabulario = Vocabulario(nome=nomePalavra,descricao=descricao, prova=Prova.objects.get(id=int(idProva)))
                    vocabulario.save() 

        elif adicionaOQue == 'novoConteudo':
            nomeConteudo = request.POST.get('campoPalavra')
            materiaConteudo_id = request.POST.get('materiaSelect')
            prova = Prova.objects.get(id=idProva)
            materia=  Materia.objects.get(id=materiaConteudo_id)
            try:
                tabelaConteudo = ConteudoPrecisoVer.objects.get(nome=nomeConteudo) #se não encontrar nada da erro ai vai pro except
                messages.add_message(request, constants.ERROR, 'Conteudo já foi colocado', extra_tags='conteudoNovoCriado') #extra_tags funciona como um name 
            except:
                conteudo = ConteudoPrecisoVer(nome=nomeConteudo,materia=materia, prova=prova)
                conteudo.save()
            # return HttpResponse(f'nome conteudo {nomeConteudo} - materia {materia}')
        elif adicionaOQue =='conteudoRever':
            nomeConteudo = request.POST.get('campoPalavra')
            materiaConteudo_id = request.POST.get('materiaSelect')
            prova = Prova.objects.get(id=idProva)
            materia=  Materia.objects.get(id=materiaConteudo_id)
            novoConteudo =ConteudoRever(
                nome  = nomeConteudo,prova= prova,materia=materia
            )

            novoConteudo.save()


    return redirect(f'/prova/corrigirProva/{idProva}')

def modificaDados(request, acao,modelName,id):
    url = request.GET.get('caminho') or request.POST.get('caminho')  
    #faz isso para pegar a url passada como  get  na hora de clicar no botão para chamar o caminho o POSt ali por causa de se for formulario o get
    # para colocar argumento numa função você usr {% url 'nome' parametros%}?nomequevocequerDarAliTaCaminho={{valorquevocequerPassarAliNoCasotarequest.path}}

    if acao == 'excluir':
       
        model = apps.get_model('app', modelName) #app ali como parâmetor por que é o lugar que a a tabela ta localizada (no palicativo chamaado app)
        if modelName == 'Questoes':
          
            numeroQuestao = int(id.split('-')[0]) #peguei o numero da questõa que ta tipo: 12 - B

            prova_id =  request.GET.get('provaId') or request.POST.get('provaId')
            prova_id = int(prova_id)
            prova = Prova.objects.get(id=prova_id)
      
            questao = Questoes.objects.get(prova=prova, numero=numeroQuestao)
            questao.delete()

          
        
        else:
            id = int(id)
         
            item = model.objects.get(id=id)
            item.delete()
         
    elif acao == 'alteraQuestao':
        id = int(id)
        model = apps.get_model('app', modelName) # ta aqui mas nem uso
        numeroQuestao = request.POST.get('numero')
        tipoAcertoErro = request.POST.get('tipoAcertoErro')
        valorMudar = eval(request.POST.get('certoErrado', '').strip().capitalize()) #eval muda o valort 'true' de string para true bool 
        prova = Prova.objects.get(id=id)
        materia_id = request.POST.get('materiaSelect')
        materia = Materia.objects.get(id=materia_id)
        try:
            
            questao= Questoes.objects.get(prova=prova,numero=numeroQuestao)
            questao.materia=materia
            questao.acertou = valorMudar
            if valorMudar == True:
                questao.tipoAcerto= tipoAcertoErro 
                questao.tipoErro = 'Não Errei'
                questaoErradaTabela = QuestoesErradas.objects.filter(questao__numero=numeroQuestao, #questao__numero acessa o camponumero da tabela questao la nomodels 
                                                                    questao__prova=prova)
                for i in questaoErradaTabela:
                    i.delete()
                

            else:
                questao.tipoAcerto ='Não acertei'
                questao.tipoErro = tipoAcertoErro
                try:
                    x = QuestoesErradas.objects.get(questao__numero=numeroQuestao,questao__prova=prova)
                    x.delete()
                finally:
                    letraMarcada = request.POST.get('letraMarcada')
                    questaoErradaTabela = QuestoesErradas(questao=questao, letraMarcada=letraMarcada)
                    questaoErradaTabela.save()
            questao.save()
        except:
            messages.add_message(request, constants.ERROR, 'A questão não existe ainda', extra_tags='questaoInexistente')
    elif acao == 'adicionaQuestao':
        id =  int(id)
         
        model = apps.get_model('app', modelName)  #ta aqui mas nem uso
        numeroQuestao = request.POST.get('numero')
        materia_id = request.POST.get('materiaSelect')
        materia = Materia.objects.get(id=materia_id)
        tipoAcertoErro = request.POST.get('tipoAcertoErro')
        status = eval(request.POST.get('certoErrado', '').strip().capitalize()) 
        prova = Prova.objects.get(id=id)
        
        verificaExistencia= Questoes.objects.filter(numero=numeroQuestao, prova=prova)

        if  verificaExistencia:
            print('Questao ja existe')
            messages.add_message(request, constants.ERROR,'Questão já existe', extra_tags='questaoJaExiste')
        else:
            if status == True:
                tipoAcerto = tipoAcertoErro
                tipoErro = 'Não Errei'
            else:
                tipoAcerto = 'Não acertei'
                tipoErro = tipoAcertoErro
            
            questao = Questoes(numero=numeroQuestao,materia=materia,prova=prova,acertou=status,tipoAcerto=tipoAcerto, tipoErro=tipoErro)
            questao.save()

            if status == False:
                QuestoesErradas(questao=questao,letraMarcada=request.POST.get('letraMarcada')).save()


    if url:
        return redirect(url)  # redireciona para o mesmo caminho da requisição

    return HttpResponse(f'Parte não programada ainda valor da ação {acao}')

def redirecionaDetalhes(request,provaId):
        return redirect(f'/detalhes/detalhesProva/{provaId}')