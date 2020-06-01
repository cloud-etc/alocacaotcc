from django.urls import path
from alocar.views.sala import addSala, altSala, delSala, permissao4

app_name='alocar'

urlpatterns = [
    #  urls das views sala
    path('addsala/', addSala, name='addsala'),
    path('altsala/<int:id>/', altSala, name='altsala'),
    path('delsala/<int:id>/', delSala, name='delsala'),
    path('permissao4/', permissao4, name='permissao4'),
]
