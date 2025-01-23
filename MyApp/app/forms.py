from django import forms
from .models import InsuranceInfos, Predictions

class InsuranceInfos_Form(forms.ModelForm):
    class Meta:
        model= InsuranceInfos
        fields = ['age', 'sex', 'bmi', 'children', 'smoker', 'region' ]

    widgets={
        'age':forms.IntegerField(),
        'sex':forms.ChoiceField( choices =( 
            ("male", "male"), 
            ("female","female") )
        ),
        'bmi':forms.FloatField(),
        'children':forms.IntegerField(),
        'smoker':forms.ChoiceField( choices =( 
            ("yes", True), 
            ("no", False) )
        ),
        'region':forms.ChoiceField( choices =( 
            ("northwest", "northwest"), 
            ("northeast", "northeast"),
            ("southwest", "southwest"),
            ("southeast","southeast") )
        ) 
    }

class Predictions_Form(forms.Form):
    class Meta:
        model= Predictions
        fields = ['charges']