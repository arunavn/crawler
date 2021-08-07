from django.contrib.auth import models
from rest_framework import serializers
from apps.userprofile.models import Profile
from django.contrib.auth.models import User
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['username', 'email','password']
        extra_kwargs= {
            'password': {'write_only': True}
        }
class ProfileRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields= ['phoneNumber', 'baseLocation', 'jobDescription', 'age']



