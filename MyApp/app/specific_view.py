from django.shortcuts import render
from django.http import Http404
from .models import InsuranceInfos, Predictions

from predictor import Predictor

def get_perdiction_page(request):
    insurance_infos = InsuranceInfos.objects.filter(user=request.user).first()
    if insurance_infos == None :
        return Http404("Aucune information trouvée pour cet utilisateur.")

    predictor = Predictor("serialized_model.pkl")

    prediction = predictor.predict(
        age=insurance_infos.age, 
        sex=insurance_infos.sex, 
        bmi=insurance_infos.bmi,
        children=insurance_infos.children,
        smoker="yes" if insurance_infos.smoker else "no", 
        region=insurance_infos.region)
    
    prediction_model = Predictions(
        user= request.user, 
        info=insurance_infos,
        charges = prediction)
    
    if request.method =="POST" :
        print("     _________________________________________")
        print("    |")
        print(f"    |        enregistrement de  : ")
        print(f"    |            request.user  = {prediction_model.user} ") 
        print(f"    |            insurance_infos.id = {prediction_model.info.id}")
        print(f"    |            charges = {prediction_model.charges}")
        print("    |__________________________________________")
        prediction_model.save()
    
    context = {
        'insurance_infos' : insurance_infos,
        'prediction' : float(int(prediction))
    }

    return render(request = request, template_name='app/prediction.html', context= context)