from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import InsuranceInfos, Predictions
from django.core.exceptions import ValidationError

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
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Confirmation ",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    username = forms.CharField(
        label="Nom d'utilisateur", 
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
    height = forms.FloatField(
        label="Taille (cm)", min_value=50, max_value=250)
    weight = forms.FloatField(
        label="Poids (kg)", min_value=30, max_value=250)
    smoker = forms.ChoiceField(label="Fumeur", choices=SMOKER_CHOICES)
    age = forms.IntegerField(label="Votre âge")
    sex = forms.ChoiceField(label="Genre", choices=SEX_CHOICES)
    region = forms.ChoiceField(label="Région", choices=REGIONS_CHOICES)
    children = forms.IntegerField(label="Nombre d'enfants")

    class Meta:
        model = InsuranceInfos
        fields = ['age', 'sex', 'smoker', 'region', 'children', 'height', 'weight']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Votre âge'}),
            'sex': forms.Select(attrs={'class': 'form-control'}, choices=SEX_CHOICES),
            'region': forms.Select(attrs={'class': 'form-control'}, choices=REGIONS_CHOICES),
            'children': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre d\'enfants'}),
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
    
#______________________________________________________________________________
#
# region imported forms.py
#______________________________________________________________________________

class PredictionsForm(forms.ModelForm):
    class Meta():
        fields = ['charges']
        model= Predictions

    charges = forms.IntegerField( label="Prime d'assurance" )
    widgets = { 'charges' : forms.NumberInput(attrs={'class': 'form-control'}) }
    
    def clean_children(self):
        children = self.cleaned_data.get('children')

        if children < 0 or children > 20:
            raise ValidationError("Le nombre d'enfants doit être compris entre 0 et 20.")
        
        return children
    
    def clean_age(self):
        age = self.cleaned_data.get('age')

        if age < 18 or age > 120:
            raise ValidationError("L'âge' doit être compris entre 18 et 120.")
        
        return age


