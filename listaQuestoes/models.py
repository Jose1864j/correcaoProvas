from django.db import models
from app.models import *
from enum import Enum


# Create your models here.
class GrauDeCertezaEnum(Enum):
    CERTEZA = "CERTEZA"
    DUVIDA = "DUVIDA"
    CHUTE = "CHUTE"
    DEFAULT = "DEFAULT"
class AlternativasEnum(Enum): # cria um enum par aprovas
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E=  "E"
    DEFAULT = "DEFAULT"

class Listas(models.Model):
    nome = models.CharField(max_length=45)
    tipo = models.CharField(max_length=20) # se é discurssiva ou de assinalar
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='Vestibulares' )

    def __str__(self):
        return self.nome
    
class QuestoesAssinalar(models.Model):
    numero = models.IntegerField()
    alternativaMarcada = models.CharField( max_length=20,
        choices=[(tag.name, tag.value) for tag in AlternativasEnum],
        default=AlternativasEnum.DEFAULT.name)
    grauDeCerteza = models.CharField( max_length=20,
        choices=[(tag.name, tag.value) for tag in GrauDeCertezaEnum],
        default=GrauDeCertezaEnum.DEFAULT.name)
    simuladoGeral = models.BooleanField()
    lista = models.ForeignKey(Listas, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.numero} - nº {self.numero}'