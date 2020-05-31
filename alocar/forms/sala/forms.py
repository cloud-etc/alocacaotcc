from django import forms
from alocar.models.sala.models import Sala


class AddSalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = '__all__'


