from django.shortcuts import render, redirect


from django.template.loader import render_to_string
from django.shortcuts import  get_object_or_404
from django.urls import reverse

from userprofile.models import ShippingAddress



def profile(request):
    shippingaddress = ShippingAddress.objects.filter(user=request.user)
    context = {'shippingaddress':shippingaddress}
    return render(request,'store/profile.html',context)

