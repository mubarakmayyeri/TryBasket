from django.urls import path
from . import views

urlpatterns = [
  path('', views.adminLogin, name='adminLogin'),
  path('otpVerification', views.otpVerification, name='otpVerification'),
  path('dashboard', views.dashboard, name='dashboard'),
  path('adminLogout', views.adminLogout, name='adminLogout'),
  
  path('accounts', views.accounts, name='accounts'),
  path('<int:id>/blockUser', views.blockUser, name='blockUser'),
  
  path('categories', views.categories, name='categories'),
  path('addCategory', views.addCategory, name='addCategory'),
  path('<int:id>/subCategories', views.subCategories, name='subCategories'),
  
  path('products', views.products, name='products'),
  path('<int:id>/deleteProduct', views.deleteProduct, name='deleteProduct'),
  path('<int:id>/editProduct', views.editProduct, name='editProduct'),
  path('addProduct', views.addProduct, name='addProduct'),
  
  path('orders', views.orders, name='orders'),
]