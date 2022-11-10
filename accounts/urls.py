from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('otpLogin/', views.otpLogin, name='otpLogin'),
  path('otpVerification', views.otpVerification, name='otpVerification'),
  path('logout/', views.logout, name='logout'),
]