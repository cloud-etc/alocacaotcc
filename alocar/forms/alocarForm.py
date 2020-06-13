from django import forms
from alocar.models.alocarModel import Alocar


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

