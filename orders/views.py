from django.shortcuts import render, redirect
import datetime
from carts.models import CartItem
from .models import Order, Address, Payment, OrderProduct
import json
from shop.models import Product
from .forms import OrderForm
from django.http import JsonResponse
from django.conf import settings
import razorpay

# Create your views here.

client =razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_KEY))

def place_order(request, total=0, quantity=0):
  current_user = request.user
  
  cart_items = CartItem.objects.filter(user=current_user)
  cart_count = cart_items.count()
  if cart_count <= 0:
    return redirect('shop')
  
  grand_total = 0
  tax = 0
  for cart_item in cart_items:
    total += (cart_item.product.price * cart_item.quantity)
    quantity += cart_item.quantity
    
  tax = (18 * total)/100
  grand_total = total + tax
  grand_total = format(grand_total, '.2f')
  
  if request.method == 'POST':
    form = OrderForm(request.POST)
    if form.is_valid():
      data = Order()
      data.user = current_user
      data.first_name = form.cleaned_data['first_name']
      data.last_name = form.cleaned_data['last_name']
      data.phone = form.cleaned_data['phone']
      data.email = form.cleaned_data['email']
      data.address_line1 = form.cleaned_data['address_line1']
      data.address_line2 = form.cleaned_data['address_line2']
      data.state = form.cleaned_data['state']
      data.district = form.cleaned_data['district']
      data.city = form.cleaned_data['city']
      data.pincode = form.cleaned_data['pincode']
      data.order_note = form.cleaned_data['order_note']
      data.order_total = grand_total
      data.tax = tax
      data.ip = request.META.get('REMOTE_ADDR')
      data.save()
      
      # generate order number
      yr = int(datetime.date.today().strftime('%Y'))
      dt = int(datetime.date.today().strftime('%d'))
      mt = int(datetime.date.today().strftime('%m'))
      d = datetime.date(yr,mt,dt)
      current_date = d.strftime("%Y%m%d") 
      order_number = current_date + str(data.id)
      data.order_number = order_number
      data.save()
      
      order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
      context = {
        'order':order,
        'cart_items':cart_items,
        'total':total,
        'tax':tax,
        'grand_total':grand_total,
        'order_number':order_number,
      }
      return render(request, 'orders/payment.html', context)
    else:
      return redirect('checkout')
    
def payments(request):
  
    body = json.loads(request.body)
    
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        order_id = order.order_number,
        payment_method = body['paymode'],
        amount_paid = order.order_total,
        status = True
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    
    cart_items = CartItem.objects.filter(user = request.user)

    for cart_item in cart_items:
        order_product =  OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id =  request.user.id
        order_product.product_id = cart_item.product_id
        order_product.quantity =  cart_item.quantity
        order_product.product_price = cart_item.product.price
        order_product.ordered = True
        order_product.save()
        
        
        product = Product.objects.get( id = cart_item.product_id)
        product.stock -= cart_item.quantity
        product.save()
    
    #clear cart
    CartItem.objects.filter(user = request.user).delete()
    #send order number and Transaction id to Web page using 

      
    data = {
        'order_number': order.order_number,
        'transID':payment.payment_id
        }
    return JsonResponse(data)
  
def payments_completed(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number = order_number)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/payment-success.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')

def cash_on_delivery(request,id):
    # Move cart item to ordered product table
    try:
        order = Order.objects.get(user = request.user, is_ordered = False, order_number = id)
        cart_items = CartItem.objects.filter(user = request.user)
        order.is_ordered = True
        payment = Payment(
            user = request.user,
            payment_id = order.order_number,
            order_id = order.order_number,
            payment_method = 'Cash On Delivery', 
            amount_paid = order.order_total,
            status = False
        )
        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        for cart_item in cart_items:
            order_product =  OrderProduct()
            order_product.order_id = order.id

            order_product.user_id =  request.user.id
            order_product.product_id = cart_item.product_id
            order_product.quantity =  cart_item.quantity
            order_product.product_price = cart_item.sub_total()
            order_product.ordered = True
            order_product.save()
            
        #Reduce Quantity of product
        
            product = Product.objects.get( id = cart_item.product_id)
            product.stock -= cart_item.quantity
            product.save()

        #clear cart
        CartItem.objects.filter(user = request.user).delete()
        #send order number and Transaction id to Web page using 
        context ={
          'orders':order,
          'payment':payment
             }
        return render(request,'orders/cod_success.html',context)
    except:
      return redirect('home')
    
def cancel_order(request,id):
    if request.user.is_superadmin:
      order = Order.objects.get(order_number = id)
    else:
      order = Order.objects.get(order_number = id,user = request.user)
    order.status = "Cancelled"
    order.save()
    payment = Payment.objects.get(order_id = order.order_number)
    payment.delete()
    if request.user.is_superadmin:
      return redirect('orders')
    else:
      return redirect('orderDetails', id)

def razorpay(request):
  current_user = request.user
  
  cart_items = CartItem.objects.filter(user=current_user)

  grand_total = 0
  tax = 0
  total = 0
  for cart_item in cart_items:
    total += (cart_item.product.price * cart_item.quantity)
    
  tax = (18 * total)/100
  grand_total = total + tax
  grand_total = format(grand_total, '.2f')
    
  amount = float(grand_total) * 100
  
  DATA = {
    "amount": amount,
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "key1": "value3",
        "key2": "value2"
    }
      }
  payment = client.order.create(data=DATA)
  return JsonResponse({
    'payment':payment,
     'payment_method' : "RazorPay"
      })
   
def test(request):
  return render(request, 'orders/test.html')