from django import forms
from .models import Predictions


class PredictionsForm(forms.ModelForm):
    class Meta():
        fields = ['charges']
        model= Predictions

    charges = forms.IntegerField( label="Prime d'assurance" )
    widgets = { 'charges' : forms.NumberInput(attrs={'class': 'form-control'}) }

    
        