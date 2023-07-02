from django.urls import path
from . import views
app_name = 'cart'

urlpatterns = [

    path('cart_add/<int:product_id>', views.cart_add, name='cart_add'),
    path('remove_cart_item', views.remove_cart_item, name='remove_cart_item'),

    path('cart_details/',views.cart_details,name='cart_details'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),

    path('myorders/',views.myorders,name='myorders'),
    path('orderdetail/<int:id>',views.orderdetail,name='orderdetail'),
    path('order_completed/', views.order_completed, name='order_completed'),

    path('show_coupons/',views.show_coupons,name='show_coupons'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('proceed_to_pay/', views.proceed_to_pay, name='proceed_to_pay'),

    path('cancel_order', views.cancel_order, name='cancel_order'),
    path('order_return', views.order_return, name='order_return'),

    path('orders/<int:order_id>/invoice/', views.download_invoice, name='download_invoice'),

    path('error_page/',views.error_page,name='error_page')
    

    
]
