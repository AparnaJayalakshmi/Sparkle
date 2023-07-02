from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from cart.models import Cart 
from accounts.models import *
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

from .models import WishlistItem
from django.contrib import messages

from django.core.paginator import Paginator



def store(request):
    products = Product.objects.all().filter(is_available=True).order_by('id')
    user= None
    email = request.session.get('email')
    phone_number = request.session.get('phone_number')
    if email or phone_number:
        user = request.user

    context = {
        'products': products,
        'user': user,
        
    }
    return render(request, 'home.html', context)


# def search(request):
#     category=Category.objects.all()
#     if 'search' in request.GET:
#         keyword=request.GET['search']
#         if keyword:
#             products=Product.objects.order_by('id').filter(product_name__icontains=keyword)
#         else:
#             return HttpResponseRedirect(request.META["HTTP_REFERER"])
      
#     context={
#         'products':products,
#         'category':category,
#         'keyword':keyword
#     }
#     return render(request,'store/store.html',context)

def view_by_category(request, id):
    category = get_object_or_404(Category, id=id)
    product_list = Product.objects.filter(category=category, is_available=True).order_by('created_date')

    paginator = Paginator(product_list, 6)  # Show 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'store/store.html', context)

def search(request):
    category=Category.objects.all()
    if 'search' in request.GET:

        keyword=request.GET['search']
        print("search working", keyword)

        if keyword:
            page_obj=Product.objects.order_by('id').filter(product_name__icontains=keyword)
        else:
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
      
    context={
        'page_obj':page_obj,
        'category':category,
        'keyword':keyword
    }
    return render(request,'store/store.html',context)



def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    context = {
        'single_product': product,
    }
    return render(request, 'store/product_detail.html', context)


def wishlist_add(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        WishlistItem.objects.get_or_create(user=request.user, product=product)
        return redirect('store:view_wishlist')
    except Exception as e:
        # Handle the error, display an error message, or redirect to an error page
        return redirect('accounts:login')

def view_wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    context = {'wishlist_items': wishlist_items}
    return render(request, 'wishlist.html', context)

def wishlist_remove(request, product_id):
    wishlist_item = get_object_or_404(WishlistItem, user=request.user, product__id=product_id)
    wishlist_item.delete()
    return redirect('store:view_wishlist')