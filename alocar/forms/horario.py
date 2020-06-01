from django import forms
from alocar.models.horario import Horario


class AddHorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = '__all__'


