from django.contrib import admin
from django.urls import path, include

from .views import testConnection, createUser, signIn, MyTokenObtainPairView, getAccountInfo
from rest_framework_simplejwt.views import (TokenRefreshView)




urlpatterns = [
    path('', testConnection, name='connectionCheck'),
    path('get-token', MyTokenObtainPairView.as_view(), name='get-token'),
    path('refresh-token', TokenRefreshView.as_view(), name='refresh-token'),
    path('create-user', createUser, name='create-container'),
    path('sign-in', signIn, name='sign-in'),
    path('get-account-info', getAccountInfo, name='get-account-info'),
]