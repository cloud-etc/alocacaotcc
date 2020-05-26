from django.conf import settings
from django.db import models
from django.urls import reverse

class Turma(models.Model):
    turma = models.CharField('Turma', max_length=8, unique=True)
    curso = models.CharField('Curso', null=False, max_length=50)
    periodo = models.CharField('Periodo', null=False, max_length=50)
    disciplina = models.CharField('Disciplina', max_length=50)
    qtdalunos = models.PositiveSmallIntegerField('Qtd')
    professor = models.CharField('Professor', max_length=50)
    internet = models.BooleanField('Internet', default=False)
    projetor = models.BooleanField('Projetor', default=False)
    computador = models.BooleanField('Computador', default=False)
    criada = models.DateTimeField('Criada', auto_now_add=True)
    alterada = models.DateTimeField('Alterada', auto_now=True)

    def __str__(self):
        return self.turma

    class Meta:
        verbose_name= "Turma"
        verbose_name_plural = "Turmas"
        ordering = ['curso', 'periodo']

    def save(self, *args, **kwargs):
        self.turma = self.turma.upper()
        self.curso = self.curso.upper()
        self.periodo = self.periodo.upper()
        self.disciplina = self.disciplina.upper()
        self.professor = self.professor.upper()
        super(Turma, self).save(*args, **kwargs)



class Bloco(models.Model):
    bloco = models.CharField('Bloco', null=False, max_length=30, unique=True)
    criada = models.DateTimeField('Criado em', auto_now_add=True)
    alterado = models.DateTimeField('Alterado', auto_now=True)

    def __str__(self):
        return self.bloco

    def save(self, *args, **kwargs):
        self.bloco = self.bloco.upper()
        super(Bloco, self).save(*args, **kwargs)


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
        
    def save(self, *args, **kwargs):
        self.sala = self.sala.upper()
        super(Sala, self).save(*args, **kwargs)


class Alocar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    data = models.DateField('Data', auto_now=True, blank=True)
    turma = models.ForeignKey(
        Turma, on_delete=models.PROTECT, related_name='alocar')
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
        ('Sábado', 'Sábado'),
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
        return self.turma.internet == True


    def sala_internet(self):
        return self.sala.internet == False



    def turma_projetor(self):
        return self.turma.projetor == True

    
    def sala_projetor(self):
        return self.sala.projetor == False


    def turma_computador(self):
        return self.turma.computador == True


    def sala_computador(self):
        return self.sala.computador == False


    class Meta:
        verbose_name = "Alocação"
        verbose_name_plural = "Alocações"
        ordering = ['turma__curso', 'turma__periodo', 'turma__disciplina']

