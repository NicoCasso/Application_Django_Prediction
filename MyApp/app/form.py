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
        # model = CustomUser
        fields = UserCreationForm.Meta.fields + ("password1", "password2", "age", "sexe", "nombre_enfants", "taille", "poids")
