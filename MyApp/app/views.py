from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

class LoginView(TemplateView):
    template_name = 'login.html'

class RegisterView(TemplateView):
    template_name = 'register.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

class PredictionView(TemplateView):
    template_name = 'prediction.html'
