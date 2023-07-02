from django.urls import path
from . import views

urlpatterns = [

    path('profile/', views.profile, name = 'profile'),
    
    # path('place_order/', views.place_order, name='place_order'),
    # path('payments/<int:order_id>/',views.payments,name='payments'),
    
    # path('myorders/',views.myorders,name='myorders'),
    # path('orderdetail/<int:id>',views.orderdetail,name='orderdetail')
    
]
