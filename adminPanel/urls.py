from django.urls import path
from . import views

urlpatterns = [
  path('', views.adminLogin, name='adminLogin'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('adminLogout/', views.adminLogout, name='adminLogout'),
  
  path('accounts/', views.accounts, name='accounts'),
  path('<int:id>/editUser/', views.editUser, name='editUser'),
  path('<int:id>/blockUser/', views.blockUser, name='blockUser'),
  
  path('categories/', views.categories, name='categories'),
  path('addCategory/', views.addCategory, name='addCategory'),
  path('<str:slug>/editCategory/', views.editCategory, name='editCategory'),
  path('<str:slug>/deleteCategory/', views.deleteCategory, name='deleteCategory'),
  
  path('<str:category_slug>/subCategories/', views.subCategories, name='subCategories'),
  path('<str:category_slug>/addSubCategory/', views.addSubCategory, name='addSubCategory'),
  path('<str:slug>/editSubCategory/', views.editSubCategory, name='editSubCategory'),
  path('<str:slug>/deleteSubCategory/', views.deleteSubCategory, name='deleteSubCategory'),
  
  path('products/', views.products, name='products'),
  path('<int:id>/deleteProduct/', views.deleteProduct, name='deleteProduct'),
  path('<int:id>/editProduct/', views.editProduct, name='editProduct'),
  path('addProduct/', views.addProduct, name='addProduct'),
  
  path('orders/', views.orders, name='orders'),
  path('update_order/<int:id>',views.update_order,name="update_order"),
]