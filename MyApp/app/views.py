
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.functional import SimpleLazyObject
from django.http import Http404
from django.core.handlers.wsgi import WSGIRequest

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib import messages

from django.views.generic import View, TemplateView, UpdateView, CreateView

from django.urls import reverse_lazy

from typing import cast

from .models import InsuranceInfos, Predictions
from .form import CustomUserCreationForm, InsuranceInfosUpdateForm, PredictionsForm

from predictor import Predictor

#______________________________________________________________________________
#
#region RegisterView
#______________________________________________________________________________
class RegisterView(CreateView):
    """
    View for user registration.

    Handles the user registration process, presenting a form to the user,
    and redirecting to the login page upon successful registration.
    """
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('app:login')

#______________________________________________________________________________
#
#region LoginView
#______________________________________________________________________________
class LoginView(TemplateView):
    """
    View for user login.

    Handles GET and POST requests for user login, including authenticating the user
    and redirecting them based on the presence of insurance information.
    """
    template_name = 'app/login.html'


    def post(self, request):
        """
        Handles POST requests for login, authenticates user and redirects.

        Args:
            request: The HTTP request object containing form data.

        Returns:
            A redirect to the user's profile or insurance info creation page.
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            # Redirect to profile if user has insurance info, otherwise to create insurance info
            redirect_url = 'app:profil' if InsuranceInfos.objects.filter(user=user).exists() else 'app:create_insurance_infos'
            return redirect(redirect_url)
        
        messages.error(request, "Incorrect username or password")
        return redirect('app:login')

#______________________________________________________________________________
#
#region HomeView
#______________________________________________________________________________
class HomeView(TemplateView):
    """
    View for the homepage.

    Displays the homepage of the application.
    """
    template_name = 'app/home.html'

#______________________________________________________________________________
#
#region ProfileView
#______________________________________________________________________________
class ProfileView(LoginRequiredMixin, TemplateView):
    """
    View for user profile page.

    Displays the user's profile and their insurance information.
    """
    template_name = 'app/profil.html'

    def get_context_data(self, **kwargs):
        """
        Adds insurance information to the context for the profile view.

        Args:
            kwargs: Additional context passed to the view.

        Returns:
            context: A dictionary containing user and insurance information.
        """
        context = super().get_context_data(**kwargs)
        context['insurance_infos'] = InsuranceInfos.objects.filter(user=self.request.user).first()
        return context

#______________________________________________________________________________
#
#region PredictionView (old)
#______________________________________________________________________________
class PredictionView(LoginRequiredMixin, TemplateView):
    """
    View for displaying and saving insurance predictions.

    Displays the user's insurance information along with a prediction of their
    insurance charges based on the provided data, and allows the user to save the prediction.
    """
    template_name = 'app/prediction.html'

    def get_context_data(self, **kwargs):
        """
        Adds prediction data to the context.

        Args:
            kwargs: Additional context passed to the view.

        Returns:
            context: A dictionary containing the prediction and insurance information.
        """
        context = super().get_context_data(**kwargs)
        insurance_infos = get_object_or_404(InsuranceInfos, user=self.request.user)

        # Create predictor and make prediction
        predictor = Predictor("serialized_model.pkl")
        prediction = predictor.predict(
            age=insurance_infos.age,
            sex=insurance_infos.sex,
            bmi=insurance_infos.bmi,
            children=insurance_infos.children,
            smoker="yes" if insurance_infos.smoker else "no",
            region=insurance_infos.region
        )

        context.update({
            'insurance_infos': insurance_infos,
            'prediction': round(prediction, 2),
            'gender': insurance_infos.get_sex_display(),
            'region': insurance_infos.get_region_display(),
            'smoker': insurance_infos.get_smoker_display()
        })
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to save the insurance prediction.

        Args:
            request: The HTTP request object containing form data.

        Returns:
            A redirect to the prediction page with a success message.
        """
        insurance_infos = get_object_or_404(InsuranceInfos, user=self.request.user)
        predictor = Predictor("serialized_model.pkl")
        prediction = predictor.predict(
            age=insurance_infos.age,
            sex=insurance_infos.sex,
            bmi=insurance_infos.bmi,
            children=insurance_infos.children,
            smoker="yes" if insurance_infos.smoker else "no",
            region=insurance_infos.region
        )

        # Save the prediction
        Predictions.objects.create(user=request.user, info=insurance_infos, charges=prediction)
        messages.success(request, "Your prediction has been saved successfully!")
        return redirect('app:prediction')
    
    @login_required
    def update_insurance_info(request):
        """
        Handles POST requests to save the insurance prediction.

        Args:
            request: The HTTP request object containing form data.

        Returns:
            A redirect to the prediction page with a success message.
        """
        # Récupérer l'objet InsuranceInfos de l'utilisateur connecté
        try:
            insurance_info = InsuranceInfos.objects.get(user=request.user)
        except InsuranceInfos.DoesNotExist:
            insurance_info = None
        
        if request.method == 'POST':
            form = InsuranceInfosUpdateForm(request.POST, instance=insurance_info)
            
            if form.is_valid():
                form.save()  # Enregistrer les données dans la base de données
                return redirect('success_url')  # Remplacez 'success_url' par l'URL de la page après l'enregistrement
        else:
            form = InsuranceInfosUpdateForm(instance=insurance_info)

        return render(request, 'path_to_your_template.html', {'form': form, 'insurance_infos': insurance_info})

#______________________________________________________________________________
#
#region UserInfosView
#______________________________________________________________________________
class UserInfosView(LoginRequiredMixin, TemplateView):
    """View for displaying user information."""
    template_name = 'app/user_infos.html'

    def get_context_data(self, **kwargs):
        """Adds user insurance information to the context."""
        context = super().get_context_data(**kwargs)
        insurance_infos = InsuranceInfos.objects.filter(user=self.request.user).first()
        if insurance_infos:
            context.update({
                'insurance_infos': insurance_infos,
                'gender': insurance_infos.get_sex_display(),
                'region': insurance_infos.get_region_display(),
                'smoker': insurance_infos.get_smoker_display()
            })
        return context

#______________________________________________________________________________
#
#region UserInfosUpdateView
#______________________________________________________________________________
class UserInfosUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user insurance information."""
    model = InsuranceInfos
    form_class = InsuranceInfosUpdateForm
    template_name = 'app/update_infos.html'
    success_url = reverse_lazy('app:user_infos')

    def get_object(self, queryset=None):
        """Returns the insurance info object for the current user."""
        return get_object_or_404(InsuranceInfos, user=self.request.user)

    def form_valid(self, form):
        """Recalculates BMI if height and weight are provided, then saves the form."""
        height, weight = form.cleaned_data.get('height'), form.cleaned_data.get('weight')
        form.instance.bmi = round(weight / ((height / 100) ** 2), 2) if height and weight else None
        return super().form_valid(form)

#______________________________________________________________________________
#
#region InsuranceInfosCreateView
#______________________________________________________________________________
class InsuranceInfosCreateView(LoginRequiredMixin, CreateView):
    """View for creating user insurance information."""
    model = InsuranceInfos
    form_class = InsuranceInfosUpdateForm
    template_name = 'app/create_insurance_infos.html'
    success_url = reverse_lazy('app:user_infos')

    def form_valid(self, form):
        """Calculates BMI, assigns user to the form, and saves the new insurance information."""
        form.instance.user = self.request.user
        height, weight = form.cleaned_data.get('height'), form.cleaned_data.get('weight')
        form.instance.bmi = round(weight / ((height / 100) ** 2), 2) if height and weight else None
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """Redirects to the update view if insurance info already exists."""
        if InsuranceInfos.objects.filter(user=self.request.user).exists():
            messages.info(request, "Your information has already been entered. You can modify it here.")
            return redirect('app:update_infos')
        return super().dispatch(request, *args, **kwargs)

#______________________________________________________________________________
#
#region get_anonymous_insurance_infos
#______________________________________________________________________________
def get_anonymous_insurance_infos() :
    """
    Generates default insurance information for anonymous users.

    Returns:
        InsuranceInfos: A populated InsuranceInfos object with default values.
    """
    insurance_infos = InsuranceInfos()
    insurance_infos.age = 18
    insurance_infos.sex = "male"
    insurance_infos.bmi = 23
    insurance_infos.children = 0
    insurance_infos.smoker = False
    insurance_infos.region = "northeast"
    insurance_infos.pk = 0 
    return insurance_infos

#______________________________________________________________________________
#
#region get_prediction_object
# user is not SimpleLazyObject
#______________________________________________________________________________
def get_predictions_object(insurance_infos : InsuranceInfos, user ) -> Predictions:
    """
    Generates a Predictions object based on the provided insurance information.

    Args:
        insurance_infos: An instance of the InsuranceInfos model.
        user: The user requesting the prediction.

    Returns:
        Predictions: A Predictions object populated with the prediction details.
    """
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
#region Prediction View with object method
#______________________________________________________________________________
class PredictionTemplateView(TemplateView):
    template_name = 'app/prediction.html'
    #template_name = 'app/prediction_original.html'
    info_form = InsuranceInfosUpdateForm
    pred_form = PredictionsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == "GET":
            info_id = self.request.GET.get("info_id")
        else :
            info_id = self.request.POST.get("info_id")

        if not info_id or info_id =="0":
            insurance_infos = InsuranceInfos.objects.filter(user=self.request.user).first()
        else :       
            insurance_infos = InsuranceInfos.objects.filter(pk=info_id).first()
        
        if not insurance_infos : 
            insurance_infos = get_anonymous_insurance_infos()
            
        self.info_form = InsuranceInfosUpdateForm(instance=insurance_infos)
        self.info_form.fields.pop('height')
        self.info_form.fields.pop('weight')

        context['info_form'] = self.info_form
        context['info_id'] = insurance_infos.pk
        context['bmi'] = insurance_infos.bmi

        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        data = cast( InsuranceInfos,self.info_form.instance)

        predictions_object = get_predictions_object(data, self.request.user)
        context['prediction'] = predictions_object.charges

        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
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
        data = cast(InsuranceInfos, self.info_form.instance )
        # do the same thing
        #data:InsuranceInfos = info_form.instance

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
            data = new_data

            self.info_form = InsuranceInfosUpdateForm(instance=data)
            self.info_form.fields.pop('height')
            self.info_form.fields.pop('weight')

        context['info_form'] = self.info_form
        context['bmi'] = data.bmi

        # info_id is included in a hidden input 
        context['info_id'] = data.pk

        predictions_object = get_predictions_object(data, self.request.user)
        predictions_object.save()

        context['prediction'] = predictions_object.charges

        return self.render_to_response( context )

def update_instance(fieldname : str, fieldvalue, data: InsuranceInfos) -> bool:
    """
    Updates the insurance information instance with new field values.

    Args:
        fieldname: The field to be updated.
        fieldvalue: The new value for the field.
        data: The InsuranceInfos instance to be updated.

    Returns:
        bool: True if any changes were made, False otherwise.
    """
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
#region unused PredictionView
#______________________________________________________________________________       
class PredictionView(LoginRequiredMixin, TemplateView):
    template_name = 'app/prediction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        insurance_infos = InsuranceInfos.objects.filter(user=self.request.user).first()

        if not insurance_infos:
            raise Http404("Aucune information trouvée pour cet utilisateur.")

        # Initialisation du prédicteur
        predictor = Predictor("serialized_model.pkl")
        prediction = predictor.predict(
            age=insurance_infos.age,
            sex=insurance_infos.sex,
            bmi=insurance_infos.bmi,
            children=insurance_infos.children,
            smoker="yes" if insurance_infos.smoker else "no",
            region=insurance_infos.region
        )
        if insurance_infos:
            context['gender'] = insurance_infos.get_sex_display()
            context['region'] = insurance_infos.get_region_display()
            context['smoker'] = insurance_infos.get_smoker_display()

        context['insurance_infos'] = insurance_infos
        context['prediction'] = float(int(prediction))

        return context

    def post(self, request, *args, **kwargs):
        insurance_infos = InsuranceInfos.objects.filter(user=self.request.user).first()

        if not insurance_infos:
            raise Http404("Aucune information trouvée pour cet utilisateur.")

        # Initialisation du prédicteur
        predictor = Predictor("serialized_model.pkl")
        prediction = predictor.predict(
            age=insurance_infos.age,
            sex=insurance_infos.sex,
            bmi=insurance_infos.bmi,
            children=insurance_infos.children,
            smoker="yes" if insurance_infos.smoker else "no",
            region=insurance_infos.region
        )

        # Création du modèle Predictions
        prediction_model = Predictions(
            user=request.user,
            info=insurance_infos,
            charges=prediction
        )

        # Enregistrement dans la base de données
        prediction_model.save()
        messages.success(request, "Votre prédiction a été enregistrée avec succès !")
        return redirect('app:prediction')


#______________________________________________________________________________
#
#region unused prediction View with functional method
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