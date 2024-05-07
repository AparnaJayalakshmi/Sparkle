from django.db import models
from store.models import Product
from accounts.models import Account
from django.utils import timezone
from userprofile.models import ShippingAddress

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateField(auto_now_add=True)
 

    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return str(self.product)
    
class Coupon(models.Model):
    couponcode = models.CharField(max_length=200, null=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    valid_from = models.DateTimeField(default=timezone.now, null=True)
    valid_to = models.DateTimeField(default=timezone.now, null=True)
    active = models.BooleanField(default=True)
    minimum_purchase = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.couponcode
    

class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(ShippingAddress,on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    total_price = models.FloatField(null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS = (
	    ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Shipped', 'Shipped'),
	    ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
            ('Returned','Returned')
    )
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    CASH_ON_DELIVERY = 'cash_on_delivery'
    RAZORPAY = 'Razorpay'
    PAYMENT_CHOICES = [
        (CASH_ON_DELIVERY, 'Cash on delivery'),
        (RAZORPAY, 'Razorpay')
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES,default=CASH_ON_DELIVERY)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField()

    # def __str__(self):
    #     return f'{self.quantity} x {self.product.name}'
    def __str__(self):
        return self.product.product_name

    def get_total_item_price(self):
        return self.product.price * self.quantity   
