from django.conf import settings
from django.db import models


class Horario(models.Model):
    horario = models.CharField('Horário', max_length=23, help_text='Ex= 00:00/00:00', unique=True)
    criado = models.DateTimeField('Criado', auto_now_add=True)
    alterado = models.DateTimeField('Alterado', auto_now=True)

    def __str__(self):
        return self.horario

    class Meta:
        verbose_name = 'Horário'
        verbose_name_plural = 'Horários'
        ordering = ['horario']



