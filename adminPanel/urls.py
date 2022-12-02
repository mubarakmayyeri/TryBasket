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
  path('category_offers/', views.category_offers, name='category_offers'),
  path('add_category_offer/', views.add_category_offer, name='add_category_offer'),
  path('delete_category_offer/<int:id>/', views.delete_category_offer, name='delete_category_offer'),
  
  path('<str:category_slug>/subCategories/', views.subCategories, name='subCategories'),
  path('<str:category_slug>/addSubCategory/', views.addSubCategory, name='addSubCategory'),
  path('<str:slug>/editSubCategory/', views.editSubCategory, name='editSubCategory'),
  path('<str:slug>/deleteSubCategory/', views.deleteSubCategory, name='deleteSubCategory'),
  
  path('products/', views.products, name='products'),
  path('<int:id>/deleteProduct/', views.deleteProduct, name='deleteProduct'),
  path('<int:id>/editProduct/', views.editProduct, name='editProduct'),
  path('addProduct/', views.addProduct, name='addProduct'),
  path('product_offers/', views.product_offers, name='product_offers'),
  path('add_product_offer/', views.add_product_offer, name='add_product_offer'),
  path('delete_product_offer/<int:id>/', views.delete_product_offer, name='delete_product_offer'),
  
  path('orders/', views.orders, name='orders'),
  path('update_order/<int:id>',views.update_order,name="update_order"),
  
  path('coupon_offers/',views.coupons,name="coupons"),
  path('add_coupon_offers/',views.add_coupon,name="add_coupon"),
  path('edit_coupon_offers/<int:id>/',views.edit_coupon,name="edit_coupon"),
  path('delete_coupon/<int:id>/',views.delete_coupon,name="delete_coupon"),
  
  path('sales_report/',views.sales_report,name="sales_report"),
    
  path('pdf_report/<str:start_date>//<str:end_date>/', views.pdf_report, name='pdf_report'),  
  path('excel_report/<str:start_date>//<str:end_date>/', views.excel_report, name='excel_report')
]