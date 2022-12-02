from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  
  path('shop/', views.shop, name='shop'),
  path('shop/<slug:category_slug>/', views.shop, name='products_by_category'),
  path('shop/<slug:category_slug>/<slug:sub_category_slug>/', views.shop, name='products_by_sub_category'),
  path('shop_filter/', views.shop, name='shop_filter'),
  
  path('shop/<slug:category_slug>/<slug:sub_category_slug>/<slug:product_slug>/', views.product_details, name='product_details'),
  
  path('price_change/', views.price_change, name='price_change'),
  
  path('contact/', views.contact, name='contact'),
]