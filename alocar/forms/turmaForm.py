from django import forms
from alocar.models.turmaModel import Turma


class AddTurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ('turma','curso','periodo','disciplina','qtdalunos',
                  'professor','internet','projetor','computador',)

