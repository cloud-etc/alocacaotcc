from django.urls import path
from alocar.views.horario import addHorario, altHorario, delHorario, permissao3


app_name='alocar'

urlpatterns = [
    #  urls das views horario
    path('addhorario/', addHorario, name='addhorario'),
    path('althorario/<int:id>/', altHorario, name='althorario'),
    path('delhorario/<int:id>/', delHorario, name='delhorario'),
    #  urls da view para exportar relatorio excel
    path('permissao3/', permissao3, name='permissao3'),

]
