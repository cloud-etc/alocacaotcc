from django.urls import path
from alocar.views.turma import addTurma, altTurma, delTurma, permissao5

app_name='alocar'

urlpatterns = [
    # urls das views turma
    path('addturma/', addTurma, name='addturma'),
    path('altturma/<int:id>/', altTurma, name='altturma'),
    path('delturma/<int:id>/', delTurma, name='delturma'),
    path('permissao5/', permissao5, name='permissao5'),
]
