from django.shortcuts import render
from django.http import Http404

from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.base_user import AbstractBaseUser

from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject

from django.views.generic import TemplateView

from .models import InsuranceInfos, Predictions
from .form import InsuranceInfosUpdateForm
from .forms import PredictionsForm

from predictor import Predictor

from typing import cast


#______________________________________________________________________________
#
#region get_anonymous_insurance_infos
#______________________________________________________________________________
def get_anonymous_insurance_infos() :
    insurance_infos = InsuranceInfos()
    insurance_infos.age = 23
    insurance_infos.sex = "male"
    insurance_infos.bmi = 23
    insurance_infos.children = 0
    insurance_infos.smoker = False
    insurance_infos.region = "northeast"
    return insurance_infos

#______________________________________________________________________________
#
#region get_prediction_object
# user is not SimpleLazyObject
#______________________________________________________________________________
def get_predictions_object(insurance_infos : InsuranceInfos, user ) -> Predictions:
    predictor = Predictor("serialized_model.pkl")
    prediction = predictor.predict(
        age=insurance_infos.age, 
        sex=insurance_infos.sex, 
        bmi=insurance_infos.bmi,
        children=insurance_infos.children,
        smoker="yes" if insurance_infos.smoker else "no", 
        region=insurance_infos.region)
    
    predictions_db_object = Predictions(
        user= user, 
        info=insurance_infos,
        charges = prediction)
    
    return predictions_db_object

#______________________________________________________________________________
#
#region View with object method
#______________________________________________________________________________
class PredictionTemplateView(TemplateView):
    template_name = 'app/prediction.html'
    info_form = InsuranceInfosUpdateForm
    pred_form = PredictionsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        insurance_infos = InsuranceInfos.objects.filter(user=self.request.user).first()
        if not insurance_infos : 
            insurance_infos = get_anonymous_insurance_infos()
            
        info_form = InsuranceInfosUpdateForm(instance=insurance_infos)
        #if self.request.method == 'GET' :
        info_form.fields.pop('height')
        info_form.fields.pop('weight')

        context['info_form'] = info_form
        context['bmi'] = insurance_infos.bmi

        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        info_form = cast( InsuranceInfosUpdateForm, context['info_form']) 

        predictions_object = get_predictions_object(info_form.instance, self.request.user)
        context['prediction'] = predictions_object.charges

        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        info_form = cast( InsuranceInfosUpdateForm, context['info_form']) 
        
        request_infos = {}
        request_infos['age'] = request.POST['age']
        request_infos['sex'] = request.POST['sex']
        request_infos['smoker'] = request.POST['smoker']
        request_infos['region'] = request.POST['region']
        request_infos['children'] = request.POST['children']
        # request_infos['height'] = request.POST['height']
        # request_infos['weight'] = request.POST['weight']
        # request_infos['bmi'] = request.POST['bmi']

        data_changed = False
        data = cast(InsuranceInfos, info_form.instance )
        for fieldname in request_infos.keys():
            data_changed |= update_instance(fieldname, request_infos[fieldname], data)

        if data_changed :
            new_data = InsuranceInfos()
            new_data.age = data.age
            new_data.sex  = data.sex
            new_data.smoker = data.smoker
            new_data.region  = data.region
            new_data.children = data.children
            new_data.bmi = data.bmi
            new_data.save()
            
            info_form.instance  = new_data
            info_form.full_clean()

        context['bmi'] = info_form.instance.bmi

        predictions_object = get_predictions_object(info_form.instance, self.request.user)
        predictions_object.save()

        context['prediction'] = predictions_object.charges

        return self.render_to_response(context)

def update_instance(fieldname : str, fieldvalue, data: InsuranceInfos) -> bool:
    data_changed = False
    match fieldname :
        case 'age' : 
            if data.age != int(fieldvalue) : 
                data.age = int(fieldvalue)
                data_changed = True

        case 'sex' : 
            if data.sex != fieldvalue :
                data.sex = fieldvalue
                data_changed = True

        case 'smoker' : 
            boolValue = True if fieldvalue == "True" else False
            if data.smoker != boolValue :
                data.smoker = boolValue
                data_changed = True
  
        case 'region' : 
            if data.region != fieldvalue :
                data.region = fieldvalue
                data_changed = True

        case 'children' :
            if data.children != int(fieldvalue) :
                data.children = int(fieldvalue)
                data_changed = True

        # case 'height' :  
        # case 'weight' : 
        # case 'bmi' : 
        #     if data.bmi != fieldvalue :
                
        #         data.bmi = ... 
        #         data_changed = True

    return data_changed
  

        




#______________________________________________________________________________
#
#region View with functional method
#______________________________________________________________________________
def get_prediction_page(request : WSGIRequest):
    if request.user is AnonymousUser : 
        insurance_infos = get_anonymous_insurance_infos()
    else :
        insurance_infos = InsuranceInfos.objects.filter(user=request.user).first()
        #return Http404("Aucune information trouvée pour cet utilisateur.")

    predictions_object = get_predictions_object(insurance_infos, request.user)
    
    if request.method =="POST" :
        print("     _________________________________________")
        print("    |")
        print(f"    |        enregistrement de  : ")
        print(f"    |            request.user  = {predictions_object.user} ") 
        print(f"    |            insurance_infos.id = {predictions_object.info.id}")
        print(f"    |            charges = {predictions_object.charges}")
        print("    |__________________________________________")
        predictions_object.save()
    
    context = {
        'insurance_infos' : insurance_infos,
        'prediction' : float(predictions_object.charges),
    }

    return render(request = request, template_name='app/prediction.html', context= context)