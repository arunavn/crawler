from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from apps.userprofile.models import Profile
from .serializers import UserRegistrationSerializer, ProfileRegistrationSerializer
from .utilities import text_extractor, download_file


@api_view(['POST'])
@permission_classes([AllowAny])
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getuser_view(request):
    user = request.user
    data, include= {}, ['username', 'email', 'phoneNumber', 'baseLocation', 'jobDescription', 'age']
    for key, value in user.__dict__.items():
            if key in include:
                data[key]= value
    try:
        profile = Profile.objects.get(user= user)
        for key, value in profile.__dict__.items():
            if key in include:
                data[key]= value
    except Profile.DoesNotExist:
        pass
    resp= Response(data)
    return resp

@api_view(['GET'])
@permission_classes([AllowAny])
def pdfcrawl_view(request):
    pdfurl= 'https://www.treasury.gov/ofac/downloads/mbs/mbslist.pdf'
    pdfFile= download_file(pdfurl)
    pdfText= text_extractor(pdfFile= pdfFile)
    data = { 'pdfData':  pdfText}
    pdfText= pdfText.replace('\n', '<br>')
    resp= Response(pdfText)
    return resp

    
