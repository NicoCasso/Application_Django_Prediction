from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from .form import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

class RegisterView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')

class LoginView(TemplateView):
    template_name = 'app/login.html'

    def connexion(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        return render(request, 'app/login.html')

class HomeView(TemplateView):
    template_name = 'app/home.html'

class ProfileView(TemplateView):
    template_name = 'app/profile.html'

class PredictionView(TemplateView):
    template_name = 'app/prediction.html'
