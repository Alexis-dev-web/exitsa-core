from django.urls import path

from .views import *


app_name = "user"

urlpatterns = [
    path('api/user', UserView.as_view(), name='user')
]

