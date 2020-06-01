from django.urls import path
from alocar.views.bloco import addBloco, altBloco, delBloco, permissao2


app_name='alocar'

urlpatterns = [
    #  urls das views bloco
    path('addbloco/', addBloco, name='addbloco'),
    path('altbloco/<int:id>/', altBloco, name='altbloco'),
    path('delbloco/<int:id>/', delBloco, name='delbloco'),
    path('permissao2/', permissao2, name='permissao2'),

]
