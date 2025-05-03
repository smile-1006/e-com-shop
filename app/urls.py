
from django.urls import path
from .views import *

urlpatterns = [
    path('', app, name="app"),  # Include the app's URLs under the 'api/' prefix
    
]