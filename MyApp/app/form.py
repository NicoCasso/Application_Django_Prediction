from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import InsuranceInfos

# définir les choix pour les régions etc dans la bdd
REGIONS_CHOICES = [
    ('southwest', 'Sud-Ouest'),
    ('northeast', 'Nord-Est'),
    ('southeast', 'Sud-Est'),
    ('northwest', 'Nord-Ouest'),
]

SEX_CHOICES = [
    ('male', 'Homme'),
    ('female', 'Femme'),
]

SMOKER_CHOICES = [
    ('yes', 'Oui'),
    ('no', 'Non'),
]

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
            'sex': forms.Select(attrs={'class': 'form-control'}, choices=SEX_CHOICES),
            'smoker': forms.Select(attrs={'class': 'form-control'}, choices=SMOKER_CHOICES),
            'region': forms.Select(attrs={'class': 'form-control'}, choices=REGIONS_CHOICES),
            'children': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre d\'enfants', 'min': 0, 'max': 20}),
        }

    def clean(self):
        cleaned_data = super().clean()
        height = cleaned_data.get("height")
        weight = cleaned_data.get("weight")
        sex = cleaned_data.get("sex")
        smoker = cleaned_data.get("smoker")
        region = cleaned_data.get("region")

        cleaned_data['sex'] = 'female' if sex == 'Femme' else 'male' if sex == 'Homme' else sex
        cleaned_data['smoker'] = 'yes' if smoker == 'Oui' else 'no' if smoker == 'Non' else smoker
        cleaned_data['region'] = {
            'Sud-Ouest': 'southwest',
            'Nord-Ouest': 'northwest',
            'Sud-Est': 'southeast',
            'Nord-Est': 'northeast'
        }.get(region, region)

        if height and weight:
            cleaned_data['bmi'] = round(weight / ((height / 100) ** 2), 2)

        return cleaned_data
