from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView
from django.http import Http404
from .models import InsuranceInfos, Predictions
from .forms import InsuranceInfos_Form

from predictor import Predictor

# class PredictionView2(View):
#     template_name = 'app/prediction.html'
#     def get(self, request):
#         return render(request, self.template_name)

class PredictionView_create(CreateView):
    model = InsuranceInfos
    form_class = InsuranceInfos_Form
    template_name = 'app/prediction.html' # spécifie le template
    context_object_name = 'insurance_infos' #le nom utilisé dans le template

    def get(self, request, *args, **kwargs):
        print(" ______________________________________________________________________")
        print("|                                                                      |")
        print("|                  PredictionView_create : GET                         |")
        print("|______________________________________________________________________|")
        self.object = InsuranceInfos()
        self.object.age=30, 
        self.object.sex="male"
        self.object.bmi=29.0
        self.object.children=2
        self.object.smoker="yes"
        self.object.region="southwest"

        #self.form_class.fields["age"] = 
        return super().get(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        print(" ______________________________________________________________________")
        print("|                                                                      |")
        print("|                  PredictionView_create : POST                        |")
        print("|______________________________________________________________________|")
        self.object = InsuranceInfos()
        self.object = None

        predictor = Predictor("serialized_model.pkl")

        age = self.object['age']
        
        #pipeline = predictor.predict()
        
        return super().post(request, *args, **kwargs)
    
class PredictionView_update(UpdateView):
    model = InsuranceInfos
    form_class = InsuranceInfos_Form
    template_name = 'app/prediction.html' # spécifie le template
    context_object_name = 'insurance_infos' #le nom utilisé dans le template

    def get(self, request, *args, **kwargs):
        print(" ______________________________________________________________________")
        print("|                                                                      |")
        print("|                  PredictionView_update : POST                        |")
        print("|______________________________________________________________________|")
        self.object = InsuranceInfos()
        self.object.age=30, 
        self.object.sex="male"
        self.object.bmi=29.0
        self.object.children=2
        self.object.smoker="yes"
        self.object.region="southwest"
        return super().get(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        print(" ______________________________________________________________________")
        print("|                                                                      |")
        print("|                  PredictionView_update : POST                        |")
        print("|______________________________________________________________________|")
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


