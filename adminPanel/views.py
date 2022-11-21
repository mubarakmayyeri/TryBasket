from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from accounts.otp import *
from django.shortcuts import get_object_or_404
from datetime import datetime,timedelta,date
from django.db.models import Sum
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.core.paginator import Paginator

from .forms import LoginForm, ProductForm, CategoryForm, SubCategoryForm, UserForm
from accounts.models import Account
from shop.models import Product
from category.models import Category, Sub_Category
from orders.models import Order, Payment

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
        
        login(request, user)
        return redirect('dashboard')
        
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
    today = datetime.today()
    today_date = today.strftime("%Y-%m-%d")
    month = today.month
    year = today.strftime("%Y")
    one_week = datetime.today() - timedelta(days=7)
    order_count_in_month = Order.objects.filter(created_at__year = year,created_at__month=month).count() 
    order_count_in_day =Order.objects.filter(created_at__date = today).count()
    order_count_in_week = Order.objects.filter(created_at__gte = one_week).count()
    number_of_users  = Account.objects.filter(is_admin = False).count()
    paypal_orders = Payment.objects.filter(payment_method="PayPal",status = True).count()
    razorpay_orders = Payment.objects.filter(payment_method="RazerPay",status = True).count()
    cash_on_delivery_count = Payment.objects.filter(payment_method="Cash On Delivery",status = True).count()

    total_payment_count = paypal_orders + razorpay_orders + cash_on_delivery_count
    try:
        total_payment_amount = Payment.objects.filter(status = True).annotate(total_amount=Cast('amount_paid', FloatField())).aggregate(Sum('total_amount'))
        
    except:
        total_payment_amount=0
    revenue = total_payment_amount['total_amount__sum']
    revenue = format(revenue, '.2f')
           
    blocked_user = Account.objects.filter(is_active = False,is_superadmin = False).count()
    unblocked_user = Account.objects.filter(is_active = True,is_superadmin = False).count()

    today_sale = Order.objects.filter(created_at__date = today_date,payment__status = True).count()
    today = today.strftime("%A")
    new_date = datetime.today() - timedelta(days = 1)
    yester_day_sale =   Order.objects.filter(created_at__date = new_date,payment__status = True).count()  
    yesterday = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_2 = Order.objects.filter(created_at__date = new_date,payment__status = True).count()
    day_2_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_3 = Order.objects.filter(created_at__date = new_date,payment__status = True).count()
    day_3_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_4 = Order.objects.filter(created_at__date = new_date,payment__status = True).count()
    day_4_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_5 = Order.objects.filter(created_at__date = new_date,payment__status = True).count()
    day_5_name = new_date.strftime("%A")
    #status
    ordered = Order.objects.filter(status = 'Order Confirmed').count()
    shipped = Order.objects.filter(status = "Shipped").count()
    out_of_delivery = Order.objects.filter(status ="Out for delivery").count()
    delivered = Order.objects.filter(status = "Delivered").count()

    context ={
        'order_count_in_month':order_count_in_month,
        'order_count_in_day':order_count_in_day,
        'order_count_in_week':order_count_in_week,
        'number_of_users':number_of_users,
        'paypal_orders':paypal_orders,
        'razorpay_orders':razorpay_orders,
        'total_payment_count':total_payment_count,
        'revenue':revenue,
        'ordered':ordered,
        'shipped':shipped,
        'out_of_delivery':out_of_delivery,
        'delivered':delivered,
        'cash_on_delivery_count':cash_on_delivery_count,
        'blocked_user':blocked_user,
        'unblocked_user':unblocked_user,
        'today_sale':today_sale,
        'yester_day_sale':yester_day_sale,
        'day_2':day_2,
        'day_3':day_3,
        'day_4':day_4,
        'day_5':day_5,
        'today':today,
        'yesterday':yesterday,
        'day_2_name':day_2_name,
        'day_3_name':day_3_name,
        'day_4_name':day_4_name,
        'day_5_name':day_5_name
        
    }
    return render(request, 'adminPanel/dashboard.html', context)
  
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
  
  paginator = Paginator(orders, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'orders':page_obj,
  }
  return render(request, 'adminPanel/orders.html', context)

@login_required(login_url = 'adminLogin')
def update_order(request, id):
  if request.method == 'POST':
    order = get_object_or_404(Order, id=id)
    status = request.POST.get('status')
    order.status = status 
    order.save()
    if status  == "Delivered":
      try:
          payment = Payment.objects.get(payment_id = order.order_number, status = False)
          print(payment)
          if payment.payment_method == 'Cash On Delivery':
              payment.status = True
              payment.save()
      except:
          pass
    order.save()
    
  return redirect('orders')