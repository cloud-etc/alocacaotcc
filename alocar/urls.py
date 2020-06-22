from django.urls import path
from alocar.views.alocarView import listAlocacao, listSalaTurma, \
    delAlocacao, home, permissao1, \
    relatorios, telapararelatorio, detalhealocacao, listalog, delog
from alocar.views.blocoView import addBloco, altBloco, delBloco
from alocar.views.horarioView import addHorario, altHorario, delHorario
from alocar.views.salaView import addSala, altSala, delSala
from alocar.views.turmaView import addTurma, altTurma, delTurma

app_name='alocar'

urlpatterns = [
    path('', home, name='home'),
    # urls das views alocacao
    path('listsalaturma/', listSalaTurma, name='listsalaturma'),
    path('listalocacao/', listAlocacao, name='listalocacao'),
    path('delalocacao/<int:id>/', delAlocacao, name='delalocacao'),
    path('detalhealocacao/<int:id>/', detalhealocacao, name='detalhealocacao'),
    # urls das views turma
    path('addturma/', addTurma, name='addturma'),
    path('altturma/<int:id>/', altTurma, name='altturma'),
    path('delturma/<int:id>/', delTurma, name='delturma'),
    #  urls das views sala
    path('addsala/', addSala, name='addsala'),
    path('altsala/<int:id>/', altSala, name='altsala'),
    path('delsala/<int:id>/', delSala, name='delsala'),
    #  urls das views bloco
    path('addbloco/', addBloco, name='addbloco'),
    path('altbloco/<int:id>/', altBloco, name='altbloco'),
    path('delbloco/<int:id>/', delBloco, name='delbloco'),
    #  urls das views horario
    path('addhorario/', addHorario, name='addhorario'),
    path('althorario/<int:id>/', altHorario, name='althorario'),
    path('delhorario/<int:id>/', delHorario, name='delhorario'),
    #  urls da view para exportar relatorio excel
    path('relatorios/', relatorios, name='relatorios'),
    path('irpararelatorio/', telapararelatorio, name='telapararelatorio'),
    # informa sobre a negacao de permissao
    path('permissao1/', permissao1, name='permissao1'),
    path('listalog/', listalog, name='listalog'),
    path('delog/<int:id>/', delog, name='delog'),
]

