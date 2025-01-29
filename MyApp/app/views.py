from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import InsuranceInfos, Predictions
from .form import CustomUserCreationForm, InsuranceInfosUpdateForm
from predictor import Predictor

class RegisterView(CreateView):
    """View for user registration."""
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('app:login')

class LoginView(TemplateView):
    """View for user login."""
    template_name = 'app/login.html'

    def post(self, request):
        """Handles POST requests for login, authenticates user."""
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

class HomeView(TemplateView):
    """View for the homepage."""
    template_name = 'app/home.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    """View for user profile page."""
    template_name = 'app/profil.html'

    def get_context_data(self, **kwargs):
        """Adds insurance information to the context."""
        context = super().get_context_data(**kwargs)
        context['insurance_infos'] = InsuranceInfos.objects.filter(user=self.request.user).first()
        return context

class PredictionView(LoginRequiredMixin, TemplateView):
    """View for displaying and saving insurance predictions."""
    template_name = 'app/prediction.html'

    def get_context_data(self, **kwargs):
        """Adds prediction data to the context."""
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
        """Handles POST requests to save the insurance prediction."""
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
