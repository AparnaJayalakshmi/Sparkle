from django.shortcuts import render
from store.models import Product
from cart.models import Cart
from django.core.paginator import Paginator

def home(request):
    product_list = Product.objects.filter(is_available=True).order_by('created_date')
    paginator = Paginator(product_list, 6)  # Show 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'store/store.html', context)


def handler404(request, exception):
    return render(request, '404.html', status=404)
