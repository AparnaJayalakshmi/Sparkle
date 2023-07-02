from django.shortcuts import render
from .models import ShippingAddress
from .forms import AddressForm
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect



# Create your views here.
def add_address(request):
    customer = request.user
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data = ShippingAddress()
            data.user = customer
            data.name = form.cleaned_data['name']
            data.phone = form.cleaned_data['phone']
            data.address = form.cleaned_data['address']
            data.pincode = form.cleaned_data['pincode']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.save()
            shippingaddress = ShippingAddress.objects.filter(user=request.user)
            context = {'shippingaddress':shippingaddress}
            return redirect('cart:cart_details')
        

    return render(request, 'add_address.html')


def edit_shipping_address(request, id):
    address = get_object_or_404(ShippingAddress, id=id)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'store/edit_address.html', {'form': form, 'address': address})

def delete_address(request,id):
    address = get_object_or_404(ShippingAddress,id=id)
    address.delete()
    return redirect('profile')

    