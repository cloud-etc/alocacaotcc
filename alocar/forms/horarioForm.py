from django import forms
from alocar.models.horarioModel import Horario


class AddHorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = '__all__'


