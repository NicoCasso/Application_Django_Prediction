from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from .views import HomeView, RegisterView, LoginView, ProfileView, PredictionView
# from django.contrib.auth.views import LoginView

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('register/', RegisterView.inscription, name='register'),
    # path('login/', LoginView.as_view(),name='login'),
    path('login/', LoginView.connexion,name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('predict', ProfileView.as_view(), name='predict'),
    # path('', RedirectView.as_view(url='home/'))
    # path('logout', views.logout, name='logout'),
    
]





# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('feature_page_1/', include('feature_page_1.urls')), # Inclure les URLs de l'application blog
#     path('', RedirectView.as_view(url='feature_page_1/'))
# ]