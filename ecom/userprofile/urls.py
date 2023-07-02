from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    
    path('add_address/', views.add_address, name='add_address'),
    path('edit_shipping_address/<int:id>',views.edit_shipping_address,name='edit_shipping_address'),
    path('delete_address/<int:id>',views.delete_address,name="delete_address")

 
]