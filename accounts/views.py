from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages, auth
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .otp import *
from requests.utils import urlparse

from carts.views import _cart_id, add_cart
from carts.models import Cart, CartItem
from orders.models import Order, OrderProduct

# Create your views here.


def register(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password']
      
      user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
      user.save()
      request.session['phone_number'] = phone_number
      
      send_otp(phone_number)
      return redirect('otpVerification')
      # messages.success(request, 'Registration Successful')  # registration without otp
      # return redirect('login')
  else:    
    form = RegistrationForm()
  context = {
    'form': form
  }
  
  return render (request, 'accounts/register.html', context)

@never_cache
def userLogin(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    user = auth.authenticate(email=email, password=password)

    if user is not None:
      
      try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
        
        if is_cart_item_exists:
          cart_item = CartItem.objects.filter(cart=cart)
          
          product_variation = []
          for item in cart_item:
            variations = item.variations.all()
            product_variation.append(list(variations))
            
          cart_item = CartItem.objects.filter(user=user)
      
          ex_var_list = []
          id = []
          for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
            
          for product in product_variation:
            if product in ex_var_list:
              index = ex_var_list.index(product)
              item_id = id[index]
              item = CartItem.objects.get(id=item_id)
              item.quantity += 1
              item.user = user
              item.save()
            else:
              cart_item = CartItem.objects.filter(cart=cart)    
              for item in cart_item:
                item.user = user
                item.save()
        
      except:
        pass
           
      auth.login(request, user)      # login without otp
      
      url = request.META.get('HTTP_REFERER')
      
      try:
        query = urlparse(url).query
        params = dict(x.split('=') for x in query.split('&'))
        if 'next' in params:
          nextPage = params['next']
          return JsonResponse(
              {'success': True,
               'url':nextPage,},
              safe=False
            )
      except:
        return JsonResponse(
          {'success': True,
           'url':'/',},
          safe=False
        )
    else:
      return JsonResponse(
        {'success':False},
        safe=False
      )
  #     # messages.success(request, 'You are now logged in.')
  #     return redirect('home')    
  #   else:
  #     messages.error(request, 'Invalid credentials')
  #     return redirect('userLogin')
    
  return render (request, 'accounts/login.html')

@never_cache
def otpLogin(request):
  if request.user.is_authenticated:
      return redirect('home')
  
  if request.method == 'POST':
    phone_number = request.POST['phone_number']
    request.session['phone_number'] = phone_number
    try:
      user = Account.objects.get(phone_number=phone_number)
    except:
      messages.error(request, 'Mobile number not registered!!!')
      return redirect('otpLogin')
    
    # send_otp(phone_number)
    return redirect('otpVerification')
  
  return render(request, 'accounts/otpLogin.html')

def otpVerification(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  phone_number = request.session['phone_number']
  
  if request.method == 'POST':
    # request.session.pop('phone_number', None)
    # request.session.modified = True
    user = Account.objects.get(phone_number=phone_number)
    try:
      check_otp = request.POST.get('otp')
      if not check_otp:
        raise e
    except Exception as e:
      messages.error(request, 'Please type in your OTP!!!')
      return redirect('otpVerification')
    
    check = verify_otp(phone_number, check_otp)
    
    if check:
      if user.is_active:
        auth.login(request, user)
        request.session['email'] = user.email
        return redirect('home')
      
      else:
        user.is_active = True
        user.save()
        messages.success(request, 'Account Verified.')
        return redirect('userLogin')
    
    else:
      messages.error(request, 'Invalid OTP!!!')
      return redirect('otpVerification')
    
  context = {
    'phone_number':phone_number
  }
  return render(request, 'accounts/otpVerification.html', context)

@login_required(login_url = 'userLogin')
def userLogout(request):
  auth.logout(request)
  messages.success(request, "You are logged out.")
  return redirect('userLogin')


# User Dashboard and Profile Settings

@login_required(login_url = 'userLogin')
def userDashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id= request.user.id, is_ordered= True)
    orders_count = orders.count()
    context = {
        'orders_count':orders_count
    }
    return render(request, 'accounts/userDashboard.html', context)
  
@login_required(login_url='userLogin')
def myOrders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')

    context = {
        'orders':orders
    }

    return render(request,'accounts/myOrders.html',context)

@login_required(login_url='userLogin') 
def orderDetails(request,order_id):
    order_details = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_details:
        subtotal += i.product_price * i.quantity
        
    context = {
        'order_details':order_details,
        'order':order,
        'subtotal':subtotal    
    }

    return render(request,'accounts/orderDetails.html',context) 