from django.db import models
from enum import Enum

# Create your models here.
class StatusEnum(Enum): # cria um enum par aprovas
    COMECADO = "começado"
    FINALIZADO = "finalizado"
    NAOINICIADO = "não iniciado"


class AreasConhecimento(models.Model):
    nome = models.CharField(max_length=200)
    def __str__(self):
        return self.nome
class Vestibular(models.Model):
    nome = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    siglaInstituicao = models.CharField(max_length=20)
    qntQuestoes  =models.IntegerField()
    areasProva = models.ManyToManyField(AreasConhecimento, related_name='Vestibulares')
    def __str__(self):
        return self.nome
    

class Materia(models.Model):
    nome = models.CharField(max_length=200)
    siglaDaMateria = models.CharField(max_length=20)
    areaPertence = models.ForeignKey(AreasConhecimento, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.nome
    
class Prova(models.Model):
    ano = models.CharField(max_length=20)
    vestibular = models.ForeignKey(Vestibular, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField( #coloca o enum das provas
        max_length=20,
        choices=[(tag.name, tag.value) for tag in StatusEnum],
        default=StatusEnum.NAOINICIADO.name
    )
    tempo_gasto = models.TimeField(blank=True, null=True, default=None)
    descricao = models.TextField(default='', blank=True, null=True)
   
    def __str__(self):
        return f"{self.vestibular} - {self.ano}"
    

class Questoes(models.Model):
    numero = models.IntegerField()
    materia = models.ForeignKey(Materia, on_delete=models.DO_NOTHING)
    prova = models.ForeignKey(Prova,on_delete=models.CASCADE)
    acertou = models.BooleanField()
    tipoAcerto = models.CharField(max_length=50, default='Não acertei')
    tipoErro = models.CharField(max_length=50, default='Não Errei')
    def __str__(self):
        return f'Q{self.numero} da {self.prova.vestibular} - {self.prova.ano}'


class Vocabulario(models.Model):
    nome = models.CharField(max_length=50)
    descricao  = models.CharField(max_length=400, default=' ')
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome

class ConteudoPrecisoVer(models.Model):
    nome = models.CharField(max_length=50)
    materia  = models.ForeignKey(Materia, on_delete=models.CASCADE)
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome

class ConteudoRever(models.Model):
    nome = models.CharField(max_length=50)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome
  
class QuestoesErradas(models.Model):
    questao = models.ForeignKey(Questoes, on_delete=models.CASCADE)
    letraMarcada = models.CharField(max_length=1)
    def __str__(self):
        return f'{self.questao.numero} da {self.questao.prova.vestibular} - {self.questao.prova.ano}'

