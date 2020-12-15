from django.db import models
class Registration(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=100)
    username=models.CharField(max_length=500)
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.username
# Create your models here.
