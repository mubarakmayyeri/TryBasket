from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from accounts.otp import *
from django.shortcuts import get_object_or_404

from .forms import LoginForm, ProductForm, CategoryForm, SubCategoryForm, UserForm
from accounts.models import Account
from shop.models import Product
from category.models import Category, Sub_Category
from orders.models import Order

# Create your views here.



# Admin log in & Logout

@never_cache
def adminLogin(request):
  if 'email' in request.session:
    return redirect('dashboard')
    
  if request.method == 'POST':
    # form = LoginForm(request.POST)
    email = request.POST['email']
    password = request.POST['password']
    
    user = authenticate(email=email, password=password)
    
    if user is not None:
      if user.is_superadmin:
        request.session['email'] = email
        
        login(request, user)            #for log in without otp
        return redirect('dashboard')
        
        # send_otp(user.phone_number)
        # return redirect('otpVerification')
      else:
        messages.error(request, 'Not Authorized!!!')
        return redirect(adminLogin)
    else:
      messages.error(request, 'Invalid login credentials')
      return redirect(adminLogin)
    
  form = LoginForm
  return render(request, 'adminPanel/login.html', {'form':form})

@login_required(login_url = 'adminLogin')
def dashboard(request):
    return render(request, 'adminPanel/dashboard.html')
  
@login_required(login_url = 'adminLogin')
def adminLogout(request):
  if 'email' in request.session:
    request.session.flush()
  logout(request)
  messages.success(request, 'Logged out successfully.')
  return redirect(adminLogin)



# User account management

@login_required(login_url = 'adminLogin')
def accounts(request):
  users = Account.objects.all().filter(is_superadmin=False).order_by('-id')
  context = {
    'users': users
  }
  return render(request, 'adminPanel/accounts.html', context)

@login_required(login_url = 'adminLogin')
def editUser(request, id):
  user = Account.objects.get(id=id)
  id = user.id
  
  if request.method == 'POST':
    form = UserForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
      form.save()
      messages.success(request, 'User Account edited successfully.')
      return redirect('accounts')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('editUser', id)
    
  else:
    form = UserForm(instance=user)
  
  context = {
    'form':form,
    'id':id,
  }
    
  return render(request, 'adminPanel/editUser.html', context)

@login_required(login_url = 'adminLogin')
def blockUser(request, id):
    users = Account.objects.get(id=id)
    if users.is_active:
        users.is_active = False
        users.save()

    else:
         users.is_active = True
         users.save()

    return redirect('accounts')



# Category Management

@login_required(login_url = 'adminLogin')
def categories(request):
  categories = Category.objects.all().order_by('id')
  context = {
    'categories':categories
  }
  return render(request, 'adminPanel/categories.html', context)

@login_required(login_url = 'adminLogin')
def addCategory(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Category added successfully.')
      return redirect('categories')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('addCategory')
  else:
    form = CategoryForm()
    context = {
      'form':form,
    }
    return render(request, 'adminPanel/addCategory.html', context)
  
@login_required(login_url = 'adminLogin')
def editCategory(request, slug):
  category = Category.objects.get(slug=slug)
  
  if request.method == 'POST':
    form = CategoryForm(request.POST, request.FILES, instance=category)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Category edited successfully.')
      return redirect('categories')
    else:
      messages.error(request, 'Invalid input')
      return redirect('editCategory', slug)
      
  form =   CategoryForm(instance=category)
  context = {
    'form':form,
    'category':category,
  }
  return render(request, 'adminPanel/editCategory.html', context)
  
@login_required(login_url = 'adminLogin')  
def deleteCategory(request, slug):
  category = Category.objects.get(slug=slug)
  category.delete()
  messages.success(request, 'Category deleted successfully.')
  return redirect('categories')


# sub category management

@login_required(login_url = 'adminLogin')
def subCategories(request, category_slug):
  subCategories = Sub_Category.objects.all().filter(category__slug=category_slug)
  context = {
    'subCategories':subCategories,
    'category_slug':category_slug,
  }
  return render(request, 'adminPanel/subCategories.html', context)

@login_required(login_url = 'adminLogin')
def addSubCategory(request, category_slug):
  if request.method == 'POST':
    form = SubCategoryForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Sub Category added successfully.')
      return redirect('subCategories', category_slug)
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('addSubCategory', category_slug)
  else:
    form = SubCategoryForm()
    context = {
      'form':form,
      'category_slug':category_slug
    }
    return render(request, 'adminPanel/addSubCategory.html', context)
  
@login_required(login_url = 'adminLogin')
def editSubCategory(request, slug):
  subCategory = Sub_Category.objects.get(slug=slug)
  cat_slug = subCategory.category.slug
  
  if request.method == 'POST':
    form = SubCategoryForm(request.POST, request.FILES, instance=subCategory)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Category edited successfully.')
      return redirect('subCategories', cat_slug)
    else:
      messages.error(request, 'Invalid input')
      return redirect('editSubCategory')
      
  form =   SubCategoryForm(instance=subCategory)
  context = {
    'form':form,
    'subCategory':subCategory,
  }
  return render(request, 'adminPanel/editSubCategory.html', context)

@login_required(login_url = 'adminLogin')  
def deleteSubCategory(request, slug):
  sub_category = Sub_Category.objects.get(slug=slug)
  cat_slug = sub_category.category.slug
  sub_category.delete()
  messages.success(request, 'Sub Category deleted successfully.')
  return redirect('subCategories', cat_slug)
 
 
 
# Product management
  
@login_required(login_url = 'adminLogin')
def products(request):
  products = Product.objects.all().order_by('-id')
  context = {
    'products': products
  }
  return render(request, 'adminPanel/products.html', context)

@login_required(login_url = 'adminLogin')
def addProduct(request):
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Product added successfully.')
      return redirect('products')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('addProduct')
  else:
    form = ProductForm()
    context = {
      'form':form,
    }
    return render(request, 'adminPanel/addProduct.html', context)

@login_required(login_url = 'adminLogin')
def editProduct(request, id):
  product = Product.objects.get(id=id)
  
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES, instance=product)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Product edited successfully.')
      return redirect('products')
    else:
      messages.error(request, 'Invalid input')
      
  form =   ProductForm(instance=product)
  context = {
    'form':form,
    'product':product,
  }
  return render(request, 'adminPanel/editProduct.html', context)

@login_required(login_url = 'adminLogin')  
def deleteProduct(request, id):
  product = Product.objects.get(id=id)
  product.delete()
  return redirect('products')



# Order Management

@login_required(login_url = 'adminLogin')
def orders(request):
  orders = Order.objects.all().order_by('-id')
  
  context = {
    'orders':orders,
  }
  return render(request, 'adminPanel/orders.html', context)

@login_required(login_url = 'adminLogin')
def update_order(request, id):
  if request.method == 'POST':
    order = get_object_or_404(Order, id=id)
    status = request.POST.get('status')
    print(status)
    order.status = status 
    order.save()
  return redirect('orders')