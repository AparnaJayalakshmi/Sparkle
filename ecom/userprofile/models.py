from django.db import models
from accounts.models import Account
from phonenumber_field.modelfields import PhoneNumberField
 
# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=50, null=True)
    phone = PhoneNumberField()
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)   

    def _str_(self):
        return str(self.id)