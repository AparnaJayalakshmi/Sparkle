from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from userprofile.models import ShippingAddress
import razorpay
from django.conf import settings
from django.core.exceptions import ValidationError
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, KeepInFrame
from io import BytesIO
# Create your views here.
from django.http import HttpResponse

@csrf_exempt
def cart_add(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        if 'quantity' in request.POST:
            selected_quantity = int(request.POST['quantity'])
        else:
            selected_quantity = 1

        cart = Cart.objects.filter(user=request.user, product=product).first()

        if cart:
            # Cart object already exists for this user and product, update quantity
            cart.quantity += selected_quantity
            cart.save()
        else:
            # Create a new cart object with the selected quantity
            cart = Cart(user=request.user, product=product, quantity=selected_quantity)
            cart.save()

        return redirect('cart:cart_details')
    except Exception as e:
        
        return redirect('accounts:login')
    
def cart_details(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_cost = 0
    for cart_item in cart_items:
        total_cost += cart_item.sub_total()

    cart_count = cart_items.count()
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_cost, 'cart_count': cart_count})

def remove_cart_item(request):
    if 'cart_item_id' in request.POST:
        cart_item_id = request.POST['cart_item_id']
        cart_item = get_object_or_404(Cart, id=cart_item_id)
        cart_item.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Cart item ID not found in request'})

# @login_required(login_url='account:user_signin')
@csrf_exempt
def update_cart_item(request):
    
    cart_items = Cart.objects.filter(user=request.user)
    cart_item_id = request.POST.get('cart_item_id')
    quantity = request.POST.get('quantity')
    product = get_object_or_404(Product, id=cart_item_id)
    cart_item = Cart.objects.filter(user=request.user, product=product).first()
    cart_item.quantity = quantity
    product_price = cart_item.product.price 
    cart_item.save()
    total_cost = 0
    for cart_item in cart_items:
        total_cost += cart_item.sub_total()
    return JsonResponse({'total_price':total_cost,'product_price':product_price})


def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    payment_method = request.POST.get('payment_option')
    total_cost = 0
    order = None
    
    if 'total_cost' in request.session:
        total_cost = request.session['total_cost']
    else:
        total_cost = sum(item.sub_total() for item in cart_items)

    cart_count = cart_items.count()

    if request.method == "POST":
        address_id = request.POST.get('address')
        address = ShippingAddress.objects.get(id=address_id)

        if payment_method == "cash_on_delivery":
            order = Order.objects.create(
                user=request.user,
                shipping_address=address,
                payment_method=payment_method,
                total_price=total_cost
            )

            for cart_item in cart_items:
                order_item = OrderProduct.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                order_item.save()

            cart_items.delete()
            request.session.pop('total_cost',None)
            order.complete = True
            order.save()

            response_data = {'success': True}
            return JsonResponse(response_data)

        else:
            order = Order.objects.create(
                user=request.user,
                shipping_address=address,
                payment_method=payment_method,
                total_price=total_cost
            )

            for cart_item in cart_items:
                order_item = OrderProduct.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                order_item.save()

            cart_items.delete()
            request.session.pop('total_cost',None)
            order.complete = True
            order.save()
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

            # Create an order on Razorpay
            razorpay_order = client.order.create(
                {
                    'amount': total_cost * 100,  # Amount is in paisa, so convert to paisa
                    'currency': 'INR',
                    'receipt': str(order.id),
                    'payment_capture': 1  # Auto capture the payment when order is placed
                }
            )

            order.razorpay_order_id = razorpay_order['id']
            order.save()

            # return render(request, 'checkout.html', {
            #     'order_id': razorpay_order['id'],
            #     'total_cost': total_cost,
            #     'cart_count': cart_count
            # })
            response_data = {'success': True}
            return JsonResponse(response_data)

    shippingaddress = ShippingAddress.objects.filter(user=request.user)
    order_id = order.id if order else None

    context = {
        'shippingaddress': shippingaddress,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'cart_count': cart_count,
        'order_id': order_id
    }

    return render(request, 'checkout.html', context)



def order_completed(request):
    # Perform any necessary actions to process the order
    
    # Render the HTML page
    return render(request, 'order_completed.html')


def myorders(request):
     orders = Order.objects.filter(user=request.user).order_by('-id')
     
     return render(request,'store/myorders.html', {'orders': orders})

def orderdetail(request, id):
    order = get_object_or_404(Order, id=id)
    orders = OrderProduct.objects.filter(order_id=id)    
    context = {
        'order': order,
        'orders': orders
    }
    return render(request,'store/orderdetail.html', context)


def show_coupons(request):
    coupons = Coupon.objects.all()
    coupon_list = [{'code': coupon.couponcode, 'discount_value': coupon.discount} for coupon in coupons]
    
    return JsonResponse({'coupons': coupon_list})

def apply_coupon(request):
    code = request.GET.get('coupon_code')

    # total_cost = float(request.GET.get('total_cost'))
    total_cost = 0
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        total_cost += item.sub_total()

    try:
        coupon = get_object_or_404(Coupon, couponcode=code, active=True)
        if coupon.minimum_purchase and total_cost < coupon.minimum_purchase:
            raise ValidationError('Minimum purchase amount not met')
        
        discount_amount = coupon.discount
        total_cost = total_cost - discount_amount

        request.session['coupon'] = code
        request.session['total_cost'] = total_cost
        response = {
            'success': True,
            'updated_cost': total_cost,
            'discount': discount_amount,
            'messages': 'Coupon applied successfully'
        }
    except (Coupon.DoesNotExist, ValidationError) as e:
        response = {
            'success': False,
            'updated_cost': total_cost,
            'messages': str(e)
        }

    return JsonResponse(response)

def proceed_to_pay(request):
    global  discount
    total_price = 0
    discount = 0
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.sub_total() for item in cart_items)
    if 'total_cost' in request.session:
        total_price = request.session['total_cost']
    
    if 'coupon' in request.session:
        coupon = request.session['coupon']
        coupon = get_object_or_404(Coupon, couponcode=coupon, active=True)
        discount = coupon.discount
    total_price = round(total_price)
    return JsonResponse({

        'total_price': total_price,
        'discount': discount,
    })

def generate_invoice(order):
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Set up the invoice content
    elements = []

    # Define custom styles
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
        name='InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.black
    )
    styles.add(custom_style)

    # Invoice title
    elements.append(Paragraph(f"Invoice for Order #{order.id}", styles['InvoiceTitle']))

    # Rest of the invoice content...
    # ...

    # Customer details
    customer_details = order.shipping_address
    customer_name = customer_details.name
    customer_address = f"{customer_details.address}, {customer_details.city}, {customer_details.state}, {customer_details.pincode}"
    customer_phone = customer_details.phone

    elements.append(Paragraph(f"Customer: {customer_name}", styles['Normal']))
    elements.append(Paragraph(f"Address: {customer_address}", styles['Normal']))
    elements.append(Paragraph(f"Phone: {customer_phone}", styles['Normal']))

    # ...

    # Product details
    product_details = [['Image', 'Product Name', 'Price']]

    styles = getSampleStyleSheet()

    for item in order.items.all():
        # Load the image and set the maximum size while maintaining aspect ratio
        image = Image(item.product.image1)
        image_width = 1.5 * inch
        image_height = (image_width * image.drawHeight) / image.drawWidth
        image.drawWidth = image_width
        image.drawHeight = image_height

        # Wrap the product name in a Paragraph to handle long names
        product_name = Paragraph(item.product.product_name, styles['Normal'])

        product_row = [
            image,
            product_name,
            str(item.product.price)
        ]
        product_details.append(product_row)

    product_table = Table(product_details, colWidths=[1.5 * inch, 3 * inch, 1 * inch])
    product_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('SIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # Left-align the table data
        ('LEFTPADDING', (0, 0), (-1, -1), 6),  # Add left padding to the table cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),  # Add right padding to the table cells
    ]))
    elements.append(product_table)

    # Save the PDF content to the buffer
    doc.build(elements)

    # Get the value of the buffer and create the response
    buffer.seek(0)
    return buffer


def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    invoice_content = generate_invoice(order)

    # Set the appropriate content type and headers for the response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{order.id}.pdf'

    # Write the PDF content to the response
    response.write(invoice_content.getvalue())
    return response

def cancel_order(request):
    order_id = request.POST.get('order_id')
    order = Order.objects.get(id=order_id)
    for item in order.items.all():
        item.product.stock += item.quantity
        item.product.save()
    order.status = 'Cancelled'
    order.save()
    return JsonResponse({"status": "Cancelled"})


def order_return(request):
    order_id = request.POST.get('order_id')
    text = request.POST.get('text')
    order = Order.objects.get(id=order_id)
    order.status = 'Returned'
    order.reason = text
    order.save()
    for item in order.items.all():
        item.product.stock += item.quantity
        item.product.save()
    return JsonResponse({'status': 'Returned'})

def error_page(request):
    return render(request,'error.html')
