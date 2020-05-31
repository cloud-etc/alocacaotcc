from django import forms
from alocar.models.bloco.models import Bloco


class AddBlocoForm(forms.ModelForm):
    class Meta:
        model = Bloco
        fields = '__all__'
