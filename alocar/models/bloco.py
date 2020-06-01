from django.db import models


class Bloco(models.Model):
    bloco = models.CharField('Bloco', null=False, max_length=30, unique=True)
    criada = models.DateTimeField('Criado em', auto_now_add=True)
    alterado = models.DateTimeField('Alterado', auto_now=True)

    def __str__(self):
        return self.bloco









