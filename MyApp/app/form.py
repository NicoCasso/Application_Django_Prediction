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







#region ___Khadija________________
class InsuranceInfosForm(forms.ModelForm):
    class Meta:
        model = InsuranceInfos
        fields = "__all__"