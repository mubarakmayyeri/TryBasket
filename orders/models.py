from django.db import models
from accounts.models import Account
from shop.models import Product, Variation

# Create your models here.

class Payment(models.Model):
    user    =  models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id =   models.CharField(max_length=100)
    order_id = models.CharField(max_length=100,blank=True)
    amount_paid     = models.CharField(max_length=100) #this is total amount paid
    created_at = models.DateTimeField(auto_now_add=True)
    paid =models.BooleanField(default=False)



    def __str__(self):
        return self.payment_id
      
class Address(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50,null=True)
    state =   models.CharField(max_length=50)
    district =   models.CharField(max_length=50)
    city =   models.CharField(max_length=50,blank=True)
    pincode =   models.CharField(max_length=50,blank=True)
    order_note = models.CharField(max_length=100, blank=True)
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def address(self):
        return f"{self.address_line1} {self.address_line2}"

    def __str__(self):
        return self.first_name

class Order(models.Model):
    STATUS = (
        ('ordered','ordered'),
        ('shipped','shipped'),
        ('out_for_delivery','out_for_delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL,null=True)
    payment= models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    # address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    order_number = models.CharField(max_length=30)
    first_name = models.CharField(max_length=50, default='')
    last_name   = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=15, default='')
    email = models.EmailField(max_length=50, default='')
    address_line1 = models.CharField(max_length=50, default='')
    address_line2 = models.CharField(max_length=50,blank=True)
    state =   models.CharField(max_length=50, default='')
    district =   models.CharField(max_length=50, default='')
    city =   models.CharField(max_length=50, default='')
    pincode =   models.IntegerField(default=0)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax     = models.FloatField()
    status = models.CharField(max_length=50,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line1} {self.address_line2}'
      
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    size = models.CharField(max_length=50,null=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(  auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.first_name