from django.shortcuts import render, redirect
from django.http  import HttpResponse
from app.models import *
from .models import *

# Create your views here.

def criarLista(request):

    if request.method == 'POST':
        nome = request.POST.get('nome').upper()
        materia_id = request.POST.get('materia')
        materia = (Materia.objects.get(id=materia_id))
        lista = Listas(
            nome=nome,
            materia=materia
        )
        lista.save()
        return redirect('/menu/iniciar/')
    
    materias = Materia.objects.all()
    return render(request, 'criarLista.html', {'materias':materias})

def listar(request):
    listas = Listas.objects.all()
    materias = Materia.objects.all();
    return render(request,'mostraListas.html', {'listas':listas,'materias': materias})

def acessarLista(request, idLista):

    lista = Listas.objects.get(id=idLista)
    if request.method == 'POST' and not QuestoesAssinalar.objects.filter(numero=int(request.POST.get('numero')),lista__id=int(idLista) ): #essa seugnda condição é apra não ter numero repetido
       
        numero = request.POST.get('numero') 
        

        alternativaDada = request.POST.get('alternativa') 
        grauDeCerteza =  request.POST.get('grauDeCerteza')
        addSimulado =  request.POST.get('addSimulado') == "on"
        enumAlternativaDada =  ''
        enumgrauDeCerteza = ''
        for i in AlternativasEnum:
            if i.name == alternativaDada:
                enumAlternativaDada = i.name
        

        for i in GrauDeCertezaEnum:
            if i.name == grauDeCerteza:
                enumgrauDeCerteza = i.name
        questao = QuestoesAssinalar(
            numero = numero,
            lista = lista, 
            alternativaMarcada=enumAlternativaDada,
            grauDeCerteza = enumgrauDeCerteza,
            simuladoGeral = addSimulado
        )
 
        questao.save()
      

    questoes =  QuestoesAssinalar.objects.filter(lista=lista)

    return render(request,"fazerLista.html", {"idLista": lista.id ,"lista":lista, "questoes":questoes})

def lancarGabarito(request, idLista):
    if request.method == "POST":
             
          lista = Listas.objects.get(id=int(idLista))
          lista.gabaritoLancado = True
          lista.save()
          for chave, valor in request.POST.items():
              if chave.startswith('inputQuestaoNumero'):
                  numero = chave.replace("inputQuestaoNumero", "")
                  
                  questao = QuestoesAssinalar.objects.get(lista__id=idLista,numero=int(numero))
                  
                  questao.letraGabarito = valor
                  
                  if str(valor) == str(questao.alternativaMarcada):
                      questao.certo = True
                  print(f'valor {valor} alternativa marcada {questao.alternativaMarcada}')

                    
                  questao.save()
         
          return redirect('finalizarLista', idLista)

    Questoeslista = QuestoesAssinalar.objects.filter(lista=int(idLista))
    lista = Listas.objects.get(id=idLista) 
    return render(request, 'lancarGabarito.html', {'Questoeslista':Questoeslista, 'lista':lista})
def finalizarLista(request, idLista):
    questoes = QuestoesAssinalar.objects.filter(lista__id=int(idLista))
    acertos = QuestoesAssinalar.objects.filter(lista__id=int(idLista), certo=True ).count()
    total  = questoes.count()
    return render(request, 'finalizarLista.html', {'questoes':questoes, 'acertos':acertos, 'total': total})
def filtrar(request, oQue):
    if request.method == 'POST':
        if oQue == 'listaDeQuestoes':
            materia =  request.POST.get('filtrarPeloQ')
            listaDeQuestoes = Listas.objects.filter(materia__nome=materia)
            materias = Materia.objects.all()
            print(listaDeQuestoes)
            return render(request,'mostraListas.html', {'listas':listaDeQuestoes,'materias':materias})