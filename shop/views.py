from django.shortcuts import render
from shop.models import Category, Product, Sub_Category

# Create your views here.

def home(request):
  categories = Category.objects.all()
  products = Product.objects.all().filter(is_available=True)
  featured_categories = Sub_Category.objects.all().filter(is_featured=True)[:5]
  featured_products = Product.objects.all().filter(is_featured=True)[:8]
  latest_products_1 = Product.objects.all().order_by('-created_date')[:3]
  latest_products_2 = Product.objects.all().order_by('-created_date')[3:6]
  
  context = {
    'categories' : categories,
    'products': products,
    'featured_categories': featured_categories,
    'featured_products': featured_products,
    'latest_products_1' : latest_products_1,
    'latest_products_2' : latest_products_2,
  }
  
  return render(request, 'home.html', context)

def shop(request):
  categories = Category.objects.all()
  products = Product.objects.all().filter(is_available=True).order_by('product_name')
  latest_products_1 = Product.objects.all().order_by('-created_date')[:3]
  latest_products_2 = Product.objects.all().order_by('-created_date')[3:6]
  poduct_count = products.count()
  
  context = {
    'categories' : categories,
    'products':products,
    'latest_products_1' : latest_products_1,
    'latest_products_2' : latest_products_2,
    'poduct_count':poduct_count
  }
  return render(request, 'shop.html', context)