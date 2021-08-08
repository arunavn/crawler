from typing import Optional
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete= models.CASCADE)

    age= models.IntegerField(null=True)
    baseLocation= models.CharField(max_length= 30, null= True)
    jobDescription= models.CharField(max_length= 200, null= True)
    phoneNumber= models.CharField(max_length= 10, null= True)

    def __str__(self):
        return self.user.username