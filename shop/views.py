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
  product_count = products.count()
  
  context = {
    'categories' : categories,
    'products':products,
    'latest_products_1' : latest_products_1,
    'latest_products_2' : latest_products_2,
    'product_count':product_count
  }
  return render(request, 'shop.html', context)

def product_details(request, category_slug, sub_category_slug, product_slug):
  try:
    product = Product.objects.get(category__slug=category_slug, sub_category__slug=sub_category_slug, slug=product_slug)
    related_products = Product.objects.filter(sub_category__slug=sub_category_slug)[:4]
  except Exception as e:
    raise e
  
  context = {
    'product':product,
    "related_products":related_products,
  }
  return render(request, 'product_detail.html', context)