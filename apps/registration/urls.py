"""All registration routes are managed here."""

from django.urls import path  # , include
from . import views

urlpatterns = [
    path('api/login/', views.LoginAPIView.as_view(), name='user_login'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='user_logout'),
]
