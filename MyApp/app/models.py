from django.db import models
from django.contrib.auth.models import User


class InsuranceInfos(models.Model):
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    bmi = models.FloatField()
    children = models.IntegerField()
    smoker = models.BooleanField()
    region = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user_id.username
    
class Predictions(models.Model):
    charges = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    info = models.ForeignKey(InsuranceInfos, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user_id.username