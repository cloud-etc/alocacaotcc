from django.urls import path
from alocar.views.alocar import listAlocacao, listSalaTurma, \
    altAlocacao, delAlocacao, home, permissao1, export_alocacoes, \
    relatorios, telapararelatorio, detalhealocacao, listalog, delog


app_name='alocar'

urlpatterns = [
    path('', home, name='home'),
    # urls das views alocacao
    path('listsalaturma/', listSalaTurma, name='listsalaturma'),
    path('listalocacao/', listAlocacao, name='listalocacao'),
    path('altalocacao/<int:id>/', altAlocacao, name='altalocacao'),
    path('delalocacao/<int:id>/', delAlocacao, name='delalocacao'),
    path('detalhealocacao/<int:id>/', detalhealocacao, name='detalhealocacao'),
    # urls da view para exportar relatorio excel
    path('todasrelatorios', export_alocacoes, name='export_alocacoes'),
    path('relatorios/', relatorios, name='relatorios'),
    path('irpararelatorio/', telapararelatorio, name='telapararelatorio'),
    # informa sobre a negacao de permissao
    path('permissao1/', permissao1, name='permissao1'),
    path('listalog/', listalog, name='listalog'),
    path('delog/<int:id>/', delog, name='delog'),
]
