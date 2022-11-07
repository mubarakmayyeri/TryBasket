from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
from accounts.models import Account
from shop.models import Product
# Create your views here.

def adminLogin(request):
  if 'email' in request.session:
    return redirect('dashboard')
  
  if request.method == 'POST':
    form = LoginForm(request.POST)
    email = request.POST['email']
    password = request.POST['password']
    
    user = authenticate(email=email, password=password)
    
    if user is not None:
      if user.is_superadmin:
        request.session['email'] = email
        login(request, user)
        return redirect(adminLogin)
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

@login_required(login_url = 'adminLogin')
def accounts(request):
  users = Account.objects.all().filter(is_superadmin=False).order_by('-id')
  context = {
    'users': users
  }
  return render(request, 'adminPanel/accounts.html', context)

@login_required(login_url = 'adminLogin')
def categories(request):
  return render(request, 'adminPanel/categories.html')

@login_required(login_url = 'adminLogin')
def products(request):
  products = Product.objects.all().order_by('-id')
  context = {
    'products': products
  }
  return render(request, 'adminPanel/products.html', context)

@login_required(login_url = 'adminLogin')
def orders(request):
  return render(request, 'adminPanel/orders.html')

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
  
def deleteProduct(request, id):
  product = Product.objects.get(id=id)
  product.delete()
  return redirect('products')