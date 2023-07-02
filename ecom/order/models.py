# from django.db import models
# from accounts.models import Account
# from store.models import Product
# from userprofile.models import ShippingAddress
# from phonenumber_field.modelfields import PhoneNumberField



# class Order(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     shipping_address = models.ForeignKey(ShippingAddress,on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     STATUS = (
# 			('Pending', 'Pending'),
#             ('Confirmed', 'Confirmed'),
#             ('Shipped', 'Shipped'),
# 			('Delivered', 'Delivered'),
#             ('Cancelled', 'Cancelled'),
#             ('Returned','Returned')
#     )
#     status = models.CharField(max_length=50, choices=STATUS, default='Pending')
#     CASH_ON_DELIVERY = 'cash_on_delivery'
#     RAZORPAY = 'Razorpay'
#     PAYMENT_CHOICES = [
#         (CASH_ON_DELIVERY, 'Cash on delivery'),
#         (RAZORPAY, 'Razorpay')
#     ]
#     payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES,default=CASH_ON_DELIVERY)

   
 
# class OrderProduct(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     quantity = models.PositiveIntegerField()

#     def __str__(self):
#         return f'{self.quantity} x {self.product.name}'

#     def get_total_item_price(self):
#         return self.product.price * self.quantity
