from django import forms
from alocar.models.alocar.models import Alocar


class AddAlocForm(forms.ModelForm):
    # turma = forms.ModelChoiceField(queryset=Turma.objects.filter(alocada=False))

    class Meta:
        model = Alocar
        fields = ('turma','sala','dia','horario')

        widgets = {
            'turma': forms.Select(attrs={'class': 'form-control'}),
            'sala': forms.Select(attrs={'class': 'form-control'}),
            'dia': forms.Select(attrs={'class': 'form-control'}),
            'horario': forms.Select(attrs={'class': 'form-control'})
        }

