from django.contrib import admin
from django.urls import path
from phone_validation.views import UserViewSet
from . import views

urlpatterns = [
    path("profile/",views.UserProfileView,name='Profile')
    # path("otp/", UserViewSet.as_view({'get': 'list'}),name='otp'),
]