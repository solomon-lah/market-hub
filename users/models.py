from django.db import models
from django.utils import timezone

# Create your models here.
class userTable(models.Model):
    email = models.EmailField(unique=True, null=False)
    passcode = models.CharField(max_length=30, null=False)
    surname = models.CharField(max_length=20, null=False)
    firstname = models.CharField(max_length=20, null=False)
    gender = models.CharField(max_length=6, null=False)
    phoneNumber = models.CharField(max_length=11, null=False)
    address = models.CharField(max_length=300, null=False)
    status = models.CharField(max_length=7,default='Allowed')
    img = models.FileField(upload_to="users/")
class itemsTable(models.Model):
    email = models.EmailField()
    itemName = models.CharField(max_length=100)
    itemPrice = models.IntegerField()
    description = models.CharField(max_length=300)
    category = models.CharField(max_length=20)
    img_1 = models.FileField(upload_to='items/')
    img_2 = models.FileField(upload_to='items/')
    dateUploaded = models.DateTimeField()
class chatTable (models.Model):
    chatId = models.CharField(max_length=100)
    message = models.CharField(max_length=3000)
    img = models.FileField(null=True, upload_to ='chat_images/' )
    sender = models.EmailField()
    receiver = models.EmailField()
    dateSent = models.DateTimeField()
    status = models.CharField(max_length=10)
    lastMessage = models.CharField(max_length=3)
class communicatingPartyId(models.Model):
    parties = models.CharField(max_length=50)

