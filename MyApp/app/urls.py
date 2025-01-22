from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('profil', ProfileView.as_view(), name='profil'),
    path('user_infos/', UserInfosView.as_view(), name='user_infos'),  # Cette ligne est importante
    path('prediction', PredictionView.as_view(), name='prediction'),
    path('update_infos/', UserInfosUpdateView.as_view(), name='update_infos'),
    path('create_insurance_infos/', InsuranceInfosCreateView.as_view(), name='create_insurance_infos'),

]
