from .models import Product

def latest_products1(request):
  latest_products_1 = Product.objects.all().order_by('-created_date')[:3]
  return dict(latest_products_1=latest_products_1)

def latest_products2(request):
  latest_products_2 = Product.objects.all().order_by('-created_date')[3:6]
  return dict(latest_products_2=latest_products_2)
