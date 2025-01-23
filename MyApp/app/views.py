from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm 
from .form import CustomUserCreationForm, InsuranceInfos, InsuranceInfosUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import InsuranceInfos


class RegisterView(TemplateView):
    template_name = 'app/register.html'

    # Vue basée sur une fonction pour le formulaire d'inscription
    def inscription(request):
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('connexion')  # Redirection vers la page de connexion après inscription
        else:
            form = CustomUserCreationForm()

        return render(request, 'app/register.html', {'form': form})

class LoginView(TemplateView):
    template_name = 'app/login.html'

    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('app:profil')  # Redirection vers la page d'accueil ou vers 'user_infos'
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
                return redirect('app:login')  # Redirection vers la page de connexion
        return render(request, self.template_name)

# Create your views here.
class HomeView(TemplateView):
    template_name = 'app/home.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'app/profil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['insurance_infos'] = InsuranceInfos.objects.get(user=self.request.user)
        except InsuranceInfos.DoesNotExist:
            context['insurance_infos'] = None
        return context


class PredictionView(TemplateView):
    template_name = 'app/prediction.html'

class UserInfosView(LoginRequiredMixin, TemplateView):
    template_name = 'app/user_infos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['insurance_infos'] = InsuranceInfos.objects.get(user=self.request.user)
        except InsuranceInfos.DoesNotExist:
            context['insurance_infos'] = None
        return context

# class UserInfosUpdateView(UpdateView):
#     model = InsuranceInfos
#     template_name = 'app/update_infos.html'
#     fields = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
#     success_url = reverse_lazy('app:user_infos')  

#     def get_object(self, queryset=None):
#         try:
#             return InsuranceInfos.objects.get(user=self.request.user)
#         except InsuranceInfos.DoesNotExist:
#             raise Http404("Aucune information trouvée pour cet utilisateur.")
class UserInfosUpdateView(UpdateView):
    model = InsuranceInfos
    form_class = InsuranceInfosUpdateForm
    template_name = 'app/update_infos.html'
    success_url = reverse_lazy('app:user_infos')

    def get_object(self, queryset=None):
        try:
            return InsuranceInfos.objects.get(user=self.request.user)
        except InsuranceInfos.DoesNotExist:
            raise Http404("Aucune information trouvée pour cet utilisateur.")

    def form_valid(self, form):
        # Recalculer le BMI si taille et poids sont dans les données nettoyées
        height = form.cleaned_data.get('height')
        weight = form.cleaned_data.get('weight')
        if height and weight:
            form.instance.bmi = round(weight / ((height / 100) ** 2), 2)
        
        # Sauvegarder le formulaire
        messages.success(self.request, "Vos informations ont été mises à jour avec succès.")
        return super().form_valid(form)



# class InsuranceInfosCreateView(LoginRequiredMixin, CreateView):
#     model = InsuranceInfos
#     form_class = InsuranceInfosForm
#     template_name = 'app/create_insurance_infos.html'
#     success_url = reverse_lazy('app:user_infos')

#     def dispatch(self, request, *args, **kwargs):
#         if InsuranceInfos.objects.filter(user=self.request.user).exists():
#             messages.info(request, "Vos informations ont déjà été saisies. Vous pouvez les modifier ici.")
#             return redirect('app:update_infos')
#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
class InsuranceInfosCreateView(LoginRequiredMixin, CreateView):
    model = InsuranceInfos
    form_class = InsuranceInfosUpdateForm
    template_name = 'app/create_insurance_infos.html'
    success_url = reverse_lazy('app:user_infos')

    def form_valid(self, form):
        # Lier l'utilisateur connecté au formulaire
        form.instance.user = self.request.user
        # Attribuer le BMI calculé
        form.instance.bmi = form.cleaned_data['bmi']
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if InsuranceInfos.objects.filter(user=self.request.user).exists():
            messages.info(request, "Vos informations ont déjà été saisies. Vous pouvez les modifier ici.")
            return redirect('app:update_infos')
        return super().dispatch(request, *args, **kwargs)