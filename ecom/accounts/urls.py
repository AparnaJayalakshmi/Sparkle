from django.urls import path 
from .import views
app_name = 'accounts'

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('login_otp', views.login_otp, name="login_otp"),
    path('verify_otp', views.verify_otp, name="verify_otp"),

    path('logout/',views.logout, name='logout'),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]