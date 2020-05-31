from django import forms
from alocar.models.turma.models import Turma


class AddTurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ('turma','curso','periodo','disciplina','qtdalunos',
                  'professor','internet','projetor','computador',)

