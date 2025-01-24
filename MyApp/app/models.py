from django.db import models
from django.contrib.auth.models import User
import uuid

class InsuranceInfos(models.Model):
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    bmi = models.FloatField(null=True, blank=True)
    children = models.IntegerField()
    smoker = models.BooleanField()
    region = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customer_number = models.CharField(max_length=10, unique=True, default=uuid.uuid4().hex[:10].upper())

    def __str__(self):
        return f"{self.user.username}" if self.user else "Unknown User"

    def get_smoker_display(self):
        return "Oui" if self.smoker else "Non"

    def get_sex_display(self):
        if self.sex == 'male':
            return 'Homme'
        elif self.sex == 'female':
            return 'Femme'
        return self.sex.capitalize()

    def get_region_display(self):
        if self.region == 'southwest':
            return 'Sud-Ouest'
        elif self.region == 'northeast':
            return 'Nord-Est'
        elif self.region == 'southeast':
            return 'Sud-Est'
        elif self.region == 'northwest':
            return 'Nord-Ouest'
        return self.region.capitalize()

    def get_full_name(self):
        return f"{self.user.first_name.capitalize()} {self.user.last_name.capitalize()}" if self.user else "Utilisateur inconnu"

class Predictions(models.Model):
    charges = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    info = models.ForeignKey(InsuranceInfos, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username if self.user else "Utilisateur inconnu"
