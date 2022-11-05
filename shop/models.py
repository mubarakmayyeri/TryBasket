from django.db import models
from category.models import Category, Sub_Category

# Create your models here.

class Product(models.Model):
  product_name = models.CharField(max_length=200, unique=True)
  slug = models.SlugField(max_length=255, unique=True)
  description = models.TextField(max_length=500, blank=True)
  price = models.IntegerField()
  image_1 = models.ImageField(upload_to='photos/products', blank=True)
  image_2 = models.ImageField(upload_to='photos/products', blank=True)
  image_3 = models.ImageField(upload_to='photos/products', blank=True)
  image_4 = models.ImageField(upload_to='photos/products', blank=True)
  stock = models.IntegerField()
  is_available = models.BooleanField(default=True)
  is_featured = models.BooleanField(default=False)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.product_name
  