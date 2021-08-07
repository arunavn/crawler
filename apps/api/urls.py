from django.urls import path
from django.urls.resolvers import URLPattern
from .views import (
    registration_view
)

app_name= 'apps.api'

urlpatterns = [
    path( 'register',  registration_view, name= 'register' )
]