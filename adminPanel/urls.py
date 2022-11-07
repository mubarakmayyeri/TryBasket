from django.urls import path
from . import views

urlpatterns = [
  path('', views.adminLogin, name='adminLogin'),
  path('dashboard', views.dashboard, name='dashboard'),
  path('adminLogout', views.adminLogout, name='adminLogout'),
  path('accounts', views.accounts, name='accounts'),
  path('categories', views.categories, name='categories'),
  path('products', views.products, name='products'),
  path('orders', views.orders, name='orders'),
  path('<int:id>/blockUser', views.blockUser, name='blockUser'),
]