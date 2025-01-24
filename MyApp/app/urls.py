from django.urls import path
from .views import HomeView, RegisterView, LoginView, ProfileView, PredictionView


urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.connexion,name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('predict', ProfileView.as_view(), name='predict'),
    
]


