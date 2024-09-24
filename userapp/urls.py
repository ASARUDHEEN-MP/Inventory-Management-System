from django.contrib import admin
from django.urls import path,include
from .views import UserRegistration,UserLogin
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("registarion",UserRegistration.as_view(),name="userRegistation"),
    path("login",UserLogin.as_view(),name="userlogin"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), 
]