from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class HomeView(View):
    template_name = 'app/home.html'
    def get(self, request):
        context = {'message': 'Welcome to the Home Page!'}
        return render(request, self.template_name, context)

class LoginView(View):
    template_name = 'app/login.html'
    def get(self, request):
        return render(request, self.template_name)
class RegisterView(View):
    template_name = 'app/register.html'
    def get(self, request):
        return render(request, self.template_name)

class ProfileView(View):
    template_name = 'app/profil.html'
    def get(self, request):
        return render(request, self.template_name)

class PredictionView(View):
    template_name = 'app/prediction.html'
    def get(self, request):
        return render(request, self.template_name)
    
class UserInfosView(View):
    template_name = 'app/user_infos.html'
    def get(self, request):
        return render(request, self.template_name)
