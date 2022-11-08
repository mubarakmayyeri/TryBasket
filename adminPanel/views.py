from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.otp import *

from .forms import LoginForm, ProductForm, CategoryForm, SubCategoryForm
from accounts.models import Account
from shop.models import Product
from category.models import Category, Sub_Category

# Create your views here.



# Admin log in & Logout

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
        # return redirect('otpVerification', email)
      else:
        messages.error(request, 'Not Authorized!!!')
        return redirect(adminLogin)
    else:
      messages.error(request, 'Invalid login credentials')
      return redirect(adminLogin)
    
  form = LoginForm
  return render(request, 'adminPanel/login.html', {'form':form})

def dashboard(request):
  if 'email' in request.session:
    return render(request, 'adminPanel/dashboard.html')
  else:
    return redirect(adminLogin)
  
@login_required(login_url = 'adminLogin')
def adminLogout(request):
  if 'email' in request.session:
    request.session.flush()
  logout(request)
  messages.success(request, 'Logged out successfully.')
  return redirect(adminLogin)

def otpVerification(request, email):
  if 'email' in request.session:
    return redirect('dashboard')
  
  if request.method == 'POST':
    user = Account.objects.get(email=email)
    phone_number = user.phone_number
    check_otp = request.POST.get('otp')
    check = verify_otp(phone_number, check_otp)
    
    if check:
      login(request, user)
      request.session['email'] = email
      return redirect('dashboard')
    
    else:
      messages.error(request, 'Invalid OTP!!!')
      return redirect('otpVerification')
    
  return render(request, 'adminPanel/otpVerification.html')



# User account management

@login_required(login_url = 'adminLogin')
def accounts(request):
  users = Account.objects.all().filter(is_superadmin=False).order_by('-id')
  context = {
    'users': users
  }
  return render(request, 'adminPanel/accounts.html', context)

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
    if form.is_valid:
      form.save()
      messages.success(request, 'Category added successfully.')
      return redirect('categories')
    else:
      messages.error(request, 'Invalid input!!!')
  else:
    form = CategoryForm()
    context = {
      'form':form,
    }
    return render(request, 'adminPanel/addCategory.html', context)
  
@login_required(login_url = 'adminLogin')  
def deleteCategory(request, id):
  category = Category.objects.get(id=id)
  category.delete()
  return redirect('categories')

@login_required(login_url = 'adminLogin')
def subCategories(request, id):
  subCategories = Sub_Category.objects.all().filter(category=id)
  context = {
    'subCategories':subCategories
  }
  return render(request, 'adminPanel/subCategories.html', context)

@login_required(login_url = 'adminLogin')
def addSubCategory(request, id):
  if request.method == 'POST':
    form = SubCategoryForm(request.POST, request.FILES)
    if form.is_valid:
      form.save()
      messages.success(request, 'Sub Category added successfully.')
      return redirect('subCategories')
    else:
      messages.error(request, 'Invalid input!!!')
  else:
    form = SubCategoryForm()
    form.category = id
    context = {
      'form':form,
    }
    return render(request, 'adminPanel/addSubCategory.html', context)

@login_required(login_url = 'adminLogin')  
def deleteSubCategory(request, id):
  sub_category = Sub_Category.objects.get(id=id)
  cat_id = sub_category.category.id
  sub_category.delete()
  return redirect('subCategories', cat_id)
 
 
 
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
    if form.is_valid:
      form.save()
      messages.success(request, 'Product added successfully.')
      return redirect('products')
    else:
      messages.error(request, 'Invalid input!!!')
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
  return render(request, 'adminPanel/orders.html')