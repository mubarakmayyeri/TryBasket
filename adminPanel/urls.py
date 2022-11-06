from django.urls import path
from . import views

urlpatterns = [
  path('', views.adminLogin, name='adminLogin'),
  path('dashboard', views.dashboard, name='dashboard'),
  path('adminLogout', views.adminLogout, name='adminLogout'),
]