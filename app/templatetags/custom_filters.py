from django import template
register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    if  dictionary.get((key)) == None: #se for uma paavra como dicionario
        return dictionary.get(str(key))
    return dictionary.get((key)) # se for um numero como chave

@register.filter(name='make_list')
def make_list(value):
    aux = []
    for i in range(1,value + 1):
        aux.append(i)

    return aux

# aqui ta criando um filtro personalizado em que pega a key de um dicionario usa lá na hora de ppegar o número de questões já feitas pq precisava de dicionarioqntQuestoesFeitas.prova.id

@register.filter(name='filtraResultado')
def filtraResultado(objeto,numeroQuestao):
    status = False
    for i in objeto:
        if i.numero  == numeroQuestao:
            status = i.acertou
    return status