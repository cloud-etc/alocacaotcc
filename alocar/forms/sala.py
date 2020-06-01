from django import forms
from alocar.models.sala import Sala


class AddSalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = '__all__'


