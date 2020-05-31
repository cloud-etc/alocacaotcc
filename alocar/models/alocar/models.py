from django.conf import settings
from django.db import models
from django.urls import reverse
from alocar.models.horario.models import Horario
from alocar.models.turma.models import Turma
from alocar.models.sala.models import Sala



class Alocar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    data = models.DateField('Data', auto_now=True, blank=True)
    turma = models.ForeignKey(
        Turma, on_delete=models.PROTECT, related_name='alocar', limit_choices_to={'alocada':False})
    sala = models.ForeignKey(
        Sala, on_delete=models.PROTECT, limit_choices_to={'disponivel': True})
    criada = models.DateTimeField('Criada', auto_now_add=True)
    alterada = models.DateTimeField('Alterada', auto_now=True)

    dias = [
        ('Segunda', 'Segunda'),
        ('Terça', 'Terça'),
        ('Quarta', 'Quarta'),
        ('Quinta', 'Quinta'),
        ('Sexta', 'Sexta'),
        ('Sabado', 'Sabado'),
    ]

    dia = models.CharField('Dia', max_length=11, choices=dias)
    horario = models.ForeignKey(
        Horario, on_delete=models.PROTECT, null=True, blank=True)

   
    def __str__(self):
        return str(' %s ' % (self.turma))


    def get_absolute_url(self):
        return reverse('alocar:listalocacao')

    
    def maior(self):
        return self.turma.qtdalunos > self.sala.capmaxima  


    def turma_internet(self):
        return self.turma.internet==True


    def sala_internet(self):
        return self.sala.internet==False

    def turma_projetor(self):
        return self.turma.projetor==True

    def sala_projetor(self):
        return self.sala.projetor==False


    def turma_computador(self):
        return self.turma.computador==True


    def sala_computador(self):
        return self.sala.computador==False


    class Meta:
        verbose_name = "Alocação"
        verbose_name_plural = "Alocações"
        ordering = ['turma__curso', 'turma__periodo', 'turma__disciplina']

