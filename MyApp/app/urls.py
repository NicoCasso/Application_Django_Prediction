from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'app'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profil/', ProfileView.as_view(), name='profil'),
    path('user_infos/', UserInfosView.as_view(), name='user_infos'),
    path('update_infos/', UserInfosUpdateView.as_view(), name='update_infos'),
    path('create_insurance_infos/', InsuranceInfosCreateView.as_view(), name='create_insurance_infos'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('prediction/', PredictionView.as_view(), name='prediction'),
]



    #path('prediction', specific_view.get_perdiction_page, name='prediction'),
# urlpatterns = [
#     path('home', HomeView.as_view(), name='home'),
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.connexion,name='login'),
#     path('profile', ProfileView.as_view(), name='profile'),
#     path('predict', ProfileView.as_view(), name='predict'),
    
# ]

# à vérifier
