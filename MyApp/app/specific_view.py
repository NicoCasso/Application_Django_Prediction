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

class PredictionView_first(CreateView):
    model = InsuranceInfos
    form_class = InsuranceInfos_Form
    template_name = 'app/prediction.html' # spécifie le template
    context_object_name = 'insurance_infos' #le nom utilisé dans le template
    #success_url = 

    def get_object(self, queryset=None):
        try:
            return InsuranceInfos.objects.get_or_create(user=self.request.user)
        except InsuranceInfos.DoesNotExist:
            raise Http404("Aucune information trouvée pour cet utilisateur.")
        
    def post(self, request, *args, **kwargs):
        self.object = None

        predictor = Predictor("serialized_model.pkl")

        age = self.object['age']
        
        #pipeline = predictor.predict()
        
        return super().post(request, *args, **kwargs)
    
class PredictionView_second(UpdateView):
    model = InsuranceInfos
    form_class = InsuranceInfos_Form
    template_name = 'app/prediction.html' # spécifie le template
    context_object_name = 'insurance_infos' #le nom utilisé dans le template

    def get_object(self, queryset=None):
        try:
            return InsuranceInfos.objects.get(user=self.request.user)
        except InsuranceInfos.DoesNotExist:
            raise Http404("Aucune information trouvée pour cet utilisateur.")
        
    def post(self, request, *args, **kwargs):
        self.object = None

        predictor = Predictor("serialized_model.pkl")

        age = self.object['age']
        
        #pipeline = predictor.predict()
        
        return super().post(request, *args, **kwargs)


