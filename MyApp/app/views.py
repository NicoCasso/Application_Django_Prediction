from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from .form import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

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

    def connexion(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('acceuil')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        return render(request, 'app/login.html')

# Create your views here.
class HomeView(TemplateView):
    template_name = 'app/home.html'


class ProfileView(TemplateView):
    template_name = 'app/profile.html'

class PredictionView(TemplateView):
    template_name = 'app/prediction.html'
