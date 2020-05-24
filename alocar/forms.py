from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import (Alocar, Sala, Turma, Bloco, Horario)


class AddAlocForm(forms.ModelForm):

    class Meta:
        model = Alocar
        fields = ('turma','sala','dia','horario')

        widgets = {
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'sala': forms.Select(attrs={'class': 'form-control'}),
            'dia': forms.Select(attrs={'class': 'form-control'}),
            'horario': forms.Select(attrs={'class': 'form-control'})
        }





       
class AddTurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ('turma','curso','periodo','disciplina','qtdalunos',
                  'professor','internet','projetor','computador',)



class AddSalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = '__all__'



class AddHorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = '__all__'



class AddBlocoForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = '__all__'
