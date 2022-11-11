from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product, Sub_Category

# Create your views here.

def home(request):
  featured_categories = Sub_Category.objects.all().filter(is_featured=True)[:5]
  featured_products = Product.objects.all().filter(is_featured=True)[:8]
  
  context = {
    'featured_categories': featured_categories,
    'featured_products': featured_products,
  }
  
  return render(request, 'home.html', context)

def shop(request, category_slug=None, sub_category_slug=None):
  categories_shop= None
  subCategories_shop = None
  products = None
  
  if category_slug != None:
    categories_shop = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.all().filter(category=categories_shop, is_available=True)
    print(categories_shop)
    product_count = products.count()
  
  elif sub_category_slug != None:
    print('hello')
    subCategories_shop = get_object_or_404(Sub_Category, slug=sub_category_slug)
    products = Product.objects.all().filter(sub_category=subCategories_shop, is_available=True)
    product_count = products.count()
    
  else:
    categories_shop = Category.objects.all()
    subCategories_shop = Sub_Category.objects.all()
    products = Product.objects.all().filter(is_available=True).order_by('product_name')
    product_count = products.count()
    
  context = {
    'categories_shop':categories_shop,
    'subCategories_shop':subCategories_shop,
    'products':products,
    'product_count':product_count
  }
  return render(request, 'shop.html', context)

def product_details(request, category_slug, sub_category_slug, product_slug):
  categories = Category.objects.all()
  
  try:
    product = Product.objects.get(category__slug=category_slug, sub_category__slug=sub_category_slug, slug=product_slug)
    
    related_products = Product.objects.filter(sub_category__slug=sub_category_slug)[:4]
  except Exception as e:
    raise e

  context = {
    'categories':categories,
    'product':product,
    "related_products":related_products,
  }
  return render(request, 'product_detail.html', context)