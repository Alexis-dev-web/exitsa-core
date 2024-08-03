from django.urls import path

from .views import *


app_name = "user"

urlpatterns = [
    path('api/user', UserView.as_view(), name='user'),
    path('api/users', UsersView.as_view(), name='users'),
    path('api/profile', ProfileView.as_view(), name='profile'),
    path('api/group', GroupView.as_view(), name='group'),
    path('api/groups', GroupsView.as_view(), name='groups')
]
