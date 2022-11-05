from django.shortcuts import render
from shop.models import Category, Product, Sub_Category

# Create your views here.

def home(request):
  categories = Category.objects.all()
  products = Product.objects.all().filter(is_available=True)
  featured_categories = Sub_Category.objects.all().filter(is_featured=True)
  featured_products = Product.objects.all().filter(is_featured=True)
  
  context = {
    'categories' : categories,
    'products': products,
    'featured_categories': featured_categories,
    'featured_products': featured_products,
  }
  return render(request, 'home.html', context)