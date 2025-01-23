from django.urls import path
from .views import HomeView, RegisterView, LoginView, ProfileView, UserInfosView
from .specific_view import PredictionView_first, PredictionView_second

app_name = 'app'
urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('profil', ProfileView.as_view(), name='profil'),
    path('user_infos', UserInfosView.as_view(), name='user_infos'),
    path('prediction', PredictionView_first.as_view(), name='prediction'),
]

    # path('logout', views.logout, name='logout'),
