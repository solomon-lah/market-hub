from django.db import models

# Create your models here.
class adminTable(models.Model):
    adminId = models.CharField(max_length=20)
    passcode = models.CharField(max_length=30)