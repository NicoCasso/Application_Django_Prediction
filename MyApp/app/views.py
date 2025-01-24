from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from .form import CustomUserCreationForm, InsuranceInfosUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import InsuranceInfos

from typing import cast

from django.views.generic import TemplateView,CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

class RegisterView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'app/register.html'

    def inscription(request):
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('connexion')
        else:
            form = CustomUserCreationForm()
        return render(request, 'app/register.html', {'form': form})
    success_url = reverse_lazy('login')


class LoginView(TemplateView):
    template_name = 'app/login.html'

    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
                return redirect('app:login')
        return render(request, self.template_name)


class HomeView(TemplateView):
    template_name = 'app/home.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'app/profil.html'


class UserInfosView(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['insurance_infos'] = InsuranceInfos.objects.filter(user=self.request.user).first()
        return context

# class PredictionView(View):
#     template_name = 'app/prediction.html'
#     def get(self, request):
#         return render(request, self.template_name)

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

class UserInfosUpdateView(UpdateView):
    model = InsuranceInfos
    form_class = InsuranceInfosUpdateForm
    template_name = 'app/update_infos.html'
    success_url = reverse_lazy('app:user_infos')

    def get_object(self, queryset=None):
        return InsuranceInfos.objects.filter(user=self.request.user).first() or Http404("Aucune information trouvée pour cet utilisateur.")

    def form_valid(self, form):
        height = form.cleaned_data.get('height')
        weight = form.cleaned_data.get('weight')

        form.instance = cast(InsuranceInfosUpdateForm, form)
     
        if height and weight:
            bmi = round(weight / ((height / 100) ** 2), 2)
            form.instance.bmi = bmi
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

        height = form.cleaned_data.get('height')
        weight = form.cleaned_data.get('weight')

        if height and weight:
            bmi = round(weight / ((height / 100) ** 2), 2)
            form.instance.bmi = bmi
        else:
            form.instance.bmi = None

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if InsuranceInfos.objects.filter(user=self.request.user).exists():
            messages.info(request, "Vos informations ont déjà été saisies. Vous pouvez les modifier ici.")
            return redirect('app:update_infos')
        return super().dispatch(request, *args, **kwargs)
