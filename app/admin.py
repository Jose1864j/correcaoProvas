from django.contrib import admin
from .models import Vestibular, AreasConhecimento,Materia, Prova, ConteudoPrecisoVer, ConteudoRever, Questoes,Vocabulario,QuestoesErradas
# Register your models here.
admin.site.register(Vestibular)
admin.site.register(AreasConhecimento)
admin.site.register(Materia)
admin.site.register(Prova)
admin.site.register(ConteudoRever)
admin.site.register(ConteudoPrecisoVer)
admin.site.register(Questoes)
admin.site.register(Vocabulario)
admin.site.register(QuestoesErradas)