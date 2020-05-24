from django.urls import path
from . import views

app_name='alocar'

urlpatterns = [
    path('', views.home, name='home'),
    # urls das views alocacao
    path('listsalaturma/', views.listSalaTurma, name='listsalaturma'),
    path('listalocacao/', views.listAlocacao, name='listalocacao'),
    path('altalocacao/<int:id>/', views.altAlocacao, name='altalocacao'),
    path('delalocacao/<int:id>/', views.delAlocacao, name='delalocacao'),
    # urls das views turma
    path('addturma/', views.addTurma, name='addturma'),
    path('conturma/', views.consultarTurmas, name='consultarturmas'),
    path('altturma/<int:id>/', views.altTurma, name='altturma'),
    path('delturma/<int:id>/', views.delTurma, name='delturma'),
    #  urls das views sala
    path('addsala/', views.addSala, name='addsala'),
    path('altsala/<int:id>/', views.altSala, name='altsala'),
    path('delsala/<int:id>/', views.delSala, name='delsala'),
    #  urls das views bloco
    path('addbloco/', views.addBloco, name='addbloco'),
    path('altbloco/<int:id>/', views.altBloco, name='altbloco'),
    path('delbloco/<int:id>/', views.delBloco, name='delbloco'),
    #  urls das views horario
    path('addhorario/', views.addHorario, name='addhorario'),
    path('althorario/<int:id>/', views.altHorario, name='althorario'),
    path('delhorario/<int:id>/', views.delHorario, name='delhorario'),
    #  urls da view para exportar relatorio excel
    path('export/xls/', views.export_alocacoes_xls, name='export_users_xls'),
    # informa sobre a negacao de permissao
    path('permissao/', views.permissao, name='permissao'),
    path('comum/', views.comum, name='comum'),
]
