from django.shortcuts import render,redirect
from accounts.models import *
from category.models import *
from store.models import *
from cart.models import *

from django.contrib.auth.models import auth

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login

# Create your views here.
@never_cache

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            request.session['email'] = email
            return redirect('customer')
        else:
            return redirect('adminlogin')

    return render(request, 'adminpanel/admin_login.html')

@login_required(login_url='adminlogin')
def adminlogout(request):
    if 'email' in  request.session:
        request.session.flush()
        return redirect ('adminlogin')



@login_required(login_url='adminlogin')
def dashboard(request):
    orders = Order.objects.filter(complete = True)
    products = Product.objects.all()
    orders_delivered = Order.objects.filter(status = 'Delivered')

    context = {'orders':orders, 'products':products, 'orders_delivered':orders_delivered}
    return render(request,'adminpanel/dashboard.html')

@login_required(login_url='adminlogin')
def customer(request):
    customers = Account.objects.all()
    context = {'customers':customers}
    return render(request,'adminpanel/customer.html', context)

@login_required(login_url='adminlogin')
def unblockcustomer(request,id):
    user=Account.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect('customer')

@login_required(login_url='adminlogin')
def blockcustomer(request,id):
    user=Account.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect('customer')

@login_required(login_url='adminlogin')
def category(request):
    category = Category.objects.all()

    return render(request,'adminpanel/category.html', {'category': category})

@login_required(login_url='adminlogin')
def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        slug =request.POST['slug']
        category = Category.objects.create(category_name=category_name,slug=slug)
        category.save()
        return redirect ('category')
    return render(request,'adminpanel/add_category.html')

@login_required(login_url='adminlogin')
def editcategory(request,id):
    if request.method == 'POST':
        category_name = request.POST['category']
        currentcategory = Category.objects.get(id=id)
        currentcategory.category_name = category_name
        
        # for product in currentcategory.products_set.all():
            
        #     product.save()
        currentcategory.save()
        return redirect ('category')

    category = Category.objects.all()
    currentcategory = Category.objects.get(id=id)
    context = { 
        'category':category,
        'currentcategory':currentcategory
         
          }

    return render(request,'adminpanel/edit_category.html', context)

@login_required(login_url='adminlogin')
def addproduct(request):
    if request.method=='GET':
        category=Category.objects.all()
        return render(request,'adminpanel/add_products.html',{'category':category})

    if request.method == 'POST':
        product_name = request.POST['product_name']        
        slug = request.POST['slug']
        price = request.POST['price']
        stock = request.POST['stock']
        category = request.POST['category']
        images = request.FILES['images']
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']
        image3 = request.FILES['image3']
     
        Product.objects.create(product_name=product_name,slug =slug,price=price,stock=stock,category_id=category,images=images,image1=image1,image2=image2,image3=image3)
        
   
        return redirect(products)
    return render(request,'adminpanel/add_products.html')

@login_required(login_url='adminlogin')
def editproduct(request,id):
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        product.product_name = request.POST['product_name']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        product.category_id = request.POST['category']
        product.description = request.POST['description']
        product.images = request.FILES.get('image', product.images)
        product.image1 = request.FILES.get('image1',product.image1)
        product.image2 = request.FILES.get('image2',product.image2)
        product.image3 = request.FILES.get('image3',product.image3)
        product.save()
        return redirect(products)
    

    category=Category.objects.all()
    product = Product.objects.get(id=id)
   
    return render (request,'adminpanel/edit_product.html', {'category':category,'product':product})

def deletecategory(request,id):
    product = Category.objects.filter(id=id)
    product.delete()
    return redirect('category')

def deleteproduct(request,id):
    product = Product.objects.filter(id=id)
    product.delete()
    return redirect('products')

@login_required(login_url='adminlogin')
def products(request):
    products =Product.objects.all()
    
    return render(request,'adminpanel/products.html',{'products':products})
 
@login_required(login_url='adminlogin')
def coupons(request):
    coupons = Coupon.objects.filter(active=True)
    context = {'coupons':coupons}
    return render(request, 'adminpanel/coupons.html', context)

@login_required(login_url='adminlogin')
def addcoupon(request):
    if request.method == 'POST':
        couponcode = request.POST['couponcode']
        discount = request.POST['discount']
        minimum_purchase= request.POST['minimum_purchase']
        Coupon.objects.create( couponcode=couponcode, discount=discount , minimum_purchase=minimum_purchase)
        return redirect('admincoupons')
    
    return render(request,  'adminpanel/add_coupon.html')
@login_required(login_url='adminlogin')
def editcoupon(request, cid):
    if request.method == 'POST':
        couponcode = request.POST['couponcode']
        discount = request.POST['discount']
        minimum_purchase = request.POST['minimum_purchase']

        coupon = Coupon.objects.get(id=cid)
        coupon.couponcode = couponcode
        coupon.discount = discount
        coupon.minimum_purchase = minimum_purchase
        
        coupon.save()
        return redirect('admincoupons')
    
    coupon = Coupon.objects.get(id=cid)
    context = {'coupon':coupon}
    return render(request,  'adminpanel/edit_coupon.html', context)

def deletecoupon(request, cid):
    coupon = Coupon.objects.get(id=cid)
    coupon.delete()
    return redirect('admincoupons')

@login_required(login_url='adminlogin')
def order(request):
    orders = Order.objects.all()
    context = {
               'orders':orders,
               
               }
    return render(request, 'adminpanel/order.html', context)

@login_required(login_url='adminlogin')
def editstatus(request,id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        return redirect('orders')
    return render(request,'adminpanel/editstatus.html')

@login_required(login_url='adminlogin')
def deleteorder(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    return redirect('orders')

@login_required(login_url='adminlogin')
def orderdetail(request, id):
    order = get_object_or_404(Order, id=id)
    order_items = OrderProduct.objects.filter(order=order)
    
    context = {
        'order_items': order_items, 
        'order':order

    }
    return render(request, 'adminpanel/order_details.html', context)