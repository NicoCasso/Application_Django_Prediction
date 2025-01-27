# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import InsuranceInfos

# Constants for choices
SEX_CHOICES = [
    ('male', 'Homme'),
    ('female', 'Femme'),
]

REGIONS_CHOICES = [
    ('southwest', 'Sud-Ouest'),
    ('northeast', 'Nord-Est'),
    ('southeast', 'Sud-Est'),
    ('northwest', 'Nord-Ouest'),
]

SMOKER_CHOICES = [
    (True, 'Oui'),
    (False, 'Non'),
]

# User Registration Form
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Mot de passe",
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Confirmation ",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    age = forms.IntegerField(
        label="Âge",
        required=True,
    )
    sexe = forms.ChoiceField(
        label="Sexe",
        choices=[('M', 'Homme'), ('F', 'Femme')],
        required=True,
    )
    nombre_enfants = forms.IntegerField(
        label="Nombre d'enfants",
        required=True,
    )
    taille = forms.IntegerField(
        label="Taille (en cm)",
        required=True,

    )
    poids = forms.IntegerField(
        label="Poids (en kg)",
        required=True,
    )

    # Custom fields for registration
    username = forms.CharField(
        label="Nom d'utilisateur",  # Changer l'étiquette
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom d\'utilisateur'})
    )
    last_name = forms.CharField(
        label="Nom",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom'})
    )
    first_name = forms.CharField(
        label="Prénom",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre prénom'})
    )
    email = forms.EmailField(
        label="Adresse email",
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Entrez votre adresse email'})
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("last_name","first_name", "email", "password1", "password2")

# Insurance Info Update Form
class InsuranceInfosUpdateForm(forms.ModelForm):
    # Fields for insurance info
    height = forms.FloatField(
        label="Taille (cm)", min_value=50, max_value=300)
    weight = forms.FloatField(
        label="Poids (kg)", min_value=10, max_value=500)
    smoker = forms.ChoiceField(label="Fumeur", choices=SMOKER_CHOICES)
    age = forms.IntegerField(label="Votre âge")
    sex = forms.ChoiceField(label="Genre", choices=SEX_CHOICES)
    region = forms.ChoiceField(label="Région", choices=REGIONS_CHOICES)
    children = forms.IntegerField(label="Nombre d'enfants")

    class Meta:
        model = InsuranceInfos
        fields = ['age', 'sex', 'smoker', 'region', 'children', 'height', 'weight']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Votre âge', 'min': 0, 'max': 120}),
            'sex': forms.Select(attrs={'class': 'form-control'}, choices=SEX_CHOICES),
            'region': forms.Select(attrs={'class': 'form-control'}, choices=REGIONS_CHOICES),
            'children': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre d\'enfants', 'min': 0, 'max': 20}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Votre taille en cm'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Votre poids en kg'}),
            'smoker': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Calcul du BMI si les deux informations sont présentes
        if self.cleaned_data.get('height') and self.cleaned_data.get('weight'):
            instance.bmi = round(self.cleaned_data['weight'] / ((self.cleaned_data['height'] / 100) ** 2), 2)

        if commit:
            instance.save()
        return instance
