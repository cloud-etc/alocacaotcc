from django.db import models
from alocar.models.bloco import Bloco


class Sala(models.Model):
    bloco = models.ForeignKey(Bloco, on_delete=models.PROTECT)
    sala = models.CharField('Sala', max_length=50, unique=True, help_text="Descrição")
    capmaxima = models.PositiveSmallIntegerField('Cap. Máxima:')
    disponivel = models.BooleanField('Disponivel', default=True)
    internet = models.BooleanField('Internet', default=False)
    projetor = models.BooleanField('Projetor', default=True)
    computador = models.BooleanField('Computador', default=False)
    criada = models.DateTimeField('Criada', auto_now_add=True)
    alterada = models.DateTimeField('Alterada ', auto_now=True)

    def __str__(self):
        return self.sala

    class Meta:
        verbose_name= "Sala"
        verbose_name_plural = "Salas"
        ordering = ['sala',]
        







