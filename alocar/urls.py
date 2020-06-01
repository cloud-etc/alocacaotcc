from django.urls import path
from alocar.views.alocar.views import listAlocacao, listSalaTurma, \
    altAlocacao, delAlocacao, home, permissao1, export_alocacoes, relatorios, telapararelatorio, detalhealocacao, \
    listalog, delog
from alocar.views.bloco.views import addBloco, altBloco, delBloco, permissao2
from alocar.views.horario.views import addHorario, altHorario, delHorario, permissao3
from alocar.views.sala.views import addSala, altSala, delSala, permissao4
from alocar.views.turma.views import addTurma, altTurma, delTurma, permissao5

app_name='alocar'

urlpatterns = [
    path('', home, name='home'),
    # urls das views alocacao
    path('listsalaturma/', listSalaTurma, name='listsalaturma'),
    path('listalocacao/', listAlocacao, name='listalocacao'),
    path('altalocacao/<int:id>/', altAlocacao, name='altalocacao'),
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
    path('todasrelatorios', export_alocacoes, name='export_alocacoes'),
    path('relatorios/', relatorios, name='relatorios'),
    path('irpararelatorio/', telapararelatorio, name='telapararelatorio'),
    # informa sobre a negacao de permissao
    path('permissao1/', permissao1, name='permissao1'),
    path('permissao2/', permissao2, name='permissao2'),
    path('permissao3/', permissao3, name='permissao3'),
    path('permissao4/', permissao4, name='permissao4'),
    path('permissao5/', permissao5, name='permissao5'),
    path('listalog/', listalog, name='listalog'),
    path('delog/<int:id>/', delog, name='delog'),
]
