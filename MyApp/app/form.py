from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import InsuranceInfos
from django.shortcuts import redirect, render

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("password1", "password2")







# #region ___Khadija________________
# class InsuranceInfosForm(forms.ModelForm):
#     class Meta:
#         model = InsuranceInfos
#         fields = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
#         widgets = {
#             'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre âge'}),
#             'sex': forms.Select(attrs={'class': 'form-control'}, choices=[('Homme', 'Homme'), ('Femme', 'Femme')]),
#             'bmi': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
#             'children': forms.NumberInput(attrs={'class': 'form-control'}),
#             'smoker': forms.Select(attrs={'class': 'form-control'}, choices=[(True, 'Oui'), (False, 'Non')]),
#             'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre région'}),
#         }
from django import forms
from .models import InsuranceInfos

REGIONS_CHOICES = [
    ('nord-ouest', 'Nord-Ouest'),
    ('sud-ouest', 'Sud-Ouest'),
    ('nord-est', 'Nord-Est'),
    ('sud-est', 'Sud-Est'),
]

# class InsuranceInfosForm(forms.ModelForm):
#     # Champs supplémentaires pour taille et poids
#     height = forms.FloatField(
#         label="Taille (cm)",
#         min_value=50,
#         max_value=300,
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Votre taille en cm'})
#     )
#     weight = forms.FloatField(
#         label="Poids (kg)",
#         min_value=10,
#         max_value=500,
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Votre poids en kg'})
#     )
class InsuranceInfosUpdateForm(forms.ModelForm):
    height = forms.FloatField(
        label="Taille (cm)",
        min_value=50,
        max_value=300,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Votre taille en cm'})
    )
    weight = forms.FloatField(
        label="Poids (kg)",
        min_value=10,
        max_value=500,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Votre poids en kg'})
    )

    class Meta:
        model = InsuranceInfos
        fields = ['age', 'sex', 'smoker', 'region', 'children']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Votre âge', 'min': 0, 'max': 120}),
            'sex': forms.Select(attrs={'class': 'form-control'}, choices=[('Homme', 'Homme'), ('Femme', 'Femme')]),
            'smoker': forms.Select(attrs={'class': 'form-control'}, choices=[(True, 'Oui'), (False, 'Non')]),
            'region': forms.Select(attrs={'class': 'form-control'}, choices=REGIONS_CHOICES),
            'children': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre d\'enfants',
                'min': 0,
                'max': 20
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get("height")
        weight = cleaned_data.get("weight")

        if height and weight:
            cleaned_data['bmi'] = round(weight / ((height / 100) ** 2), 2)

        return cleaned_data
