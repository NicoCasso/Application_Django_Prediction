from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import InsuranceInfos
from .form import CustomUserCreationForm, InsuranceInfosUpdateForm

class RegisterView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('app:login')


class LoginView(TemplateView):
    template_name = 'app/login.html'

    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                if hasattr(user, 'insuranceinfos'):
                    return redirect('app:profil')
                else:
                    return redirect('app:create_insurance_infos')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
                return redirect('app:login')
        return render(request, self.template_name)


class HomeView(TemplateView):
    template_name = 'app/home.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'app/profil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['insurance_infos'] = InsuranceInfos.objects.filter(user=self.request.user).first()
        return context


class PredictionView(View):
    template_name = 'app/prediction.html'

    def get(self, request):
        return render(request, self.template_name)


class UserInfosView(LoginRequiredMixin, TemplateView):
    template_name = 'app/user_infos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        insurance_info = InsuranceInfos.objects.filter(user=self.request.user).first()

        if insurance_info:
            context['gender'] = insurance_info.get_sex_display()
            context['region'] = insurance_info.get_region_display()
            context['smoker'] = insurance_info.get_smoker_display()

        context['insurance_infos'] = insurance_info
        return context


class UserInfosUpdateView(LoginRequiredMixin, UpdateView):
    model = InsuranceInfos
    form_class = InsuranceInfosUpdateForm
    template_name = 'app/update_infos.html'
    success_url = reverse_lazy('app:user_infos')

    def get_object(self, queryset=None):
        # Utilise `get_object_or_404` pour une meilleure gestion d'erreur
        return get_object_or_404(InsuranceInfos, user=self.request.user)

    def form_valid(self, form):
        # Calcul du BMI s'il y a la taille et le poids
        height = form.cleaned_data.get('height')
        weight = form.cleaned_data.get('weight')
        if height and weight:
            form.instance.bmi = round(weight / ((height / 100) ** 2), 2)
        else:
            form.instance.bmi = None

        messages.success(self.request, "Vos informations ont été mises à jour avec succès.")
        return super().form_valid(form)


class InsuranceInfosCreateView(LoginRequiredMixin, CreateView):
    model = InsuranceInfos
    form_class = InsuranceInfosUpdateForm
    template_name = 'app/create_insurance_infos.html'
    success_url = reverse_lazy('app:user_infos')

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Calcul du BMI s'il y a la taille et le poids
        height = form.cleaned_data.get('height')
        weight = form.cleaned_data.get('weight')
        if height and weight:
            form.instance.bmi = round(weight / ((height / 100) ** 2), 2)
        else:
            form.instance.bmi = None

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if InsuranceInfos.objects.filter(user=self.request.user).exists():
            messages.info(request, "Vos informations ont déjà été saisies. Vous pouvez les modifier ici.")
            return redirect('app:update_infos')
        return super().dispatch(request, *args, **kwargs)
