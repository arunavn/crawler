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
class WebSerializer(serializers.Serializer):
    ctl00_MainContent_ddlType = serializers.CharField(max_length = 100)
    ctl00_MainContent_txtAddress = serializers.CharField(max_length = 100)
    ctl00_MainContent_txtLastName = serializers.CharField(max_length = 100)
    ctl00_MainContent_txtCity = serializers.CharField(max_length = 100)
    ctl00_MainContent_txtID = serializers.CharField(max_length = 100)
    ctl00_MainContent_txtState = serializers.CharField(max_length = 100)
    ctl00_MainContent_lstPrograms = serializers.ListField(max_length = 100)
    ctl00_MainContent_ddlCountry = serializers.CharField(max_length = 100)
    ctl00_MainContent_ddlList = serializers.CharField(max_length = 100)
    ctl00_MainContent_Slider1_Boundcontrol = serializers.CharField(max_length = 100)
    ctl00_MainContent_btnSearch = serializers.CharField(max_length = 100)