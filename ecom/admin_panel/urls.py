from django.urls import path
from . import views


urlpatterns = [
    path('',views.adminlogin,name='adminlogin'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('dashboard', views.dashboard,name='dashboard'),

    path('customer',views.customer,name='customer'),
    path('customer/blockcustomer/<int:id>',views.blockcustomer,name='blockcustomer'),
    path('customer/unblockcustomer/<int:id>',views.unblockcustomer,name='unblockcustomer'),

    path('category/',views.category,name='category'),
    path('category/addcategory',views.addcategory,name='addcategory'),
    path('category/editcategory/<int:id>',views.editcategory,name='editcategory'),
    path('category/deletecategory/<int:id>',views.deletecategory,name='deletecategory'),

    path('products/',views.products,name='products'),
    path('products/addproduct/',views.addproduct,name='addproduct'),
    path('products/editproduct/<int:id>',views.editproduct,name='editproduct'),
    path('products/deleteproduct/<int:id>',views.deleteproduct,name='deleteproduct'),

    path('coupons/', views.coupons, name = 'admincoupons'),
    path('coupons/addcoupon/', views.addcoupon, name = 'addcoupon'),
    path('coupons/editcoupon/<int:cid>/', views.editcoupon, name = 'editcoupon'),
    path('coupons/deletecoupon/<int:cid>/', views.deletecoupon, name = 'deletecoupon'),

    
    path('orders/',views.order,name="orders"),
    path('order/deleteorder/<int:id>/',views.deleteorder, name = 'deleteorder'),
    path('editstatus/<int:id>/',views.editstatus,name="editstatus"),

    path('orderdetail/<int:id>/',views.orderdetail,name="orderdetail")

]
