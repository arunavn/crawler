from django.urls import path
from django.urls.resolvers import URLPattern
from rest_framework.authtoken import views
from .views import (
    getuser_view,
    pdfcrawl_view,
    registration_view
)


app_name= 'apps.api'

urlpatterns = [
    path( 'register',  registration_view, name= 'register' ),
    path('signin', views.obtain_auth_token),
    path('userdetails', getuser_view),
    path('pdfcrawl', pdfcrawl_view)   
    
]