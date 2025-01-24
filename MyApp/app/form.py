from django import forms
from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label="Confirmation de mot de passe",
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

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("password1", "password2")


class InsuranceInfosUpdateForm(forms.ModelForm):
    height = forms.FloatField(
        label="Taille (cm)",
        min_value=50,
        max_value=300
    )
    weight = forms.FloatField(
        label="Poids (kg)",
        min_value=10,
        max_value=500
    )
    smoker = forms.ChoiceField(
        label="Fumeur",
        choices=SMOKER_CHOICES
    )
    age = forms.IntegerField(
        label="Votre âge"
    )
    sex = forms.ChoiceField(
        label="Genre",
        choices=SEX_CHOICES
    )
    region = forms.ChoiceField(
        label="Région",
        choices=REGIONS_CHOICES
    )
    children = forms.IntegerField(
        label="Nombre d'enfants"
    )

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

        instance.smoker = self.cleaned_data['smoker']

        height = self.cleaned_data.get('height')
        weight = self.cleaned_data.get('weight')
        if height and weight:
            instance.bmi = round(weight / ((height / 100) ** 2), 2)

        if commit:
            instance.save()
        return instance
        # model = CustomUser
        fields = UserCreationForm.Meta.fields + ("password1", "password2", "age", "sexe", "nombre_enfants", "taille", "poids")
