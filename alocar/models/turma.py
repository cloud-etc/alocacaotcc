from django.db import models

class Turma(models.Model):
    turma = models.CharField('Turma', max_length=8, unique=True)
    curso = models.CharField('Curso', null=False, max_length=50)
    periodo = models.CharField('Periodo', null=False, max_length=50)
    disciplina = models.CharField('Disciplina', null=False, max_length=50)
    qtdalunos = models.PositiveSmallIntegerField('Qtd')
    alocada = models.BooleanField('Alocada', default=False)
    professor = models.CharField('Professor', max_length=50)
    internet = models.BooleanField('Internet', default=False)
    projetor = models.BooleanField('Projetor', default=False)
    computador = models.BooleanField('Computador', default=False)
    criada = models.DateTimeField('Criada', auto_now_add=True)
    alterada = models.DateTimeField('Alterada', auto_now=True)

    def __str__(self):
        return self.turma

    def esta_alocada(self):
        self.alocada = True
        self.save()

    def nao_alocada(self):
        self.alocada = False
        self.save()
    class Meta:
        verbose_name= "Turma"
        verbose_name_plural = "Turmas"
        ordering = ['curso', 'periodo']







