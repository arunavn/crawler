from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserRegistrationSerializer, ProfileRegistrationSerializer

@api_view(['POST'])
def registration_view(request):
    usrSerializer= UserRegistrationSerializer(data= request.data)
    proSerializer= ProfileRegistrationSerializer(data= request.data)
    data, include= {}, ['username', 'email', 'phoneNumber', 'baseLocation', 'jobDescription', 'age']
    u, p= usrSerializer.is_valid(), proSerializer.is_valid()
    if u and p :
        user= usrSerializer.create(usrSerializer.validated_data)
        #validated_data= usrSerializer.validate()
        user.set_password(usrSerializer.validated_data['password'])
        user.save()
        profile= proSerializer.save(user= user)
        profile.save()
        for key, value in user.__dict__.items():
            if key in include:
                data[key]= value
        for key, value in profile.__dict__.items():
            if key in include:
                data[key]= value
        resp= Response(data)
        resp.status_code= 201
    else:
        data= usrSerializer.errors
        data.update(proSerializer.errors)
        resp= Response(data)
        resp.status_code= 400
    return resp
    
