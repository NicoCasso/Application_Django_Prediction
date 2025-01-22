from django.urls import path
from .views import HomeView, RegisterView, LoginView, ProfileView, PredictionView

app_name = 'app'
urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('predict', PredictionView.as_view(), name='predict'),
]

    # path('logout', views.logout, name='logout'),
