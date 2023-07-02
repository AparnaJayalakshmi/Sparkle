from django.shortcuts import render,redirect
from .forms import OTPVerificationForm,OTPForm
from .models import *
from django.contrib import messages
from django.contrib.auth.models import auth
import random
from twilio.rest import Client
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str


def login(request):
    email = request.session.get('email')
    phone_number = request.session.get('phone_number')
    if email or phone_number:
        return redirect('store:store')

    if request.method == 'POST':
        email = request.POST['email']
        password= request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['email']=email
            # messages.info(request, 'Logged in successfully')
            return redirect('store:store')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('accounts:login')
        

    return render(request,'accounts/login.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        phonenumber = request.POST['phone_number']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if Account.objects.filter(email=email).exists():
                return redirect('accounts:register')
            else:
                user = Account.objects.create_user(first_name=fname,last_name=lname,email=email,phone_number=phonenumber,password=password)
                user.save()
                activateEmail(request,user,email)
                return redirect('accounts:login')
        else:
            messages.info(request,'Password do not match')
            return redirect('register')


    return render(request,'accounts/register.html')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        # messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('accounts:login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('accounts:login')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user.first_name}, please go to you email {to_email} inbox and click on \
                    received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')



def send_otp(phone_number):
    # Generate a 6-digit OTP
    otp = random.randint(000000, 999999)

    # Set up the Twilio client
    account_sid = 'AC2185aef335a441a783b0d642dbc7ac43'
    auth_token = '7f7a7b573ea587349bf5215c4a4e0b9f'
    client = Client(account_sid, auth_token)

    # Send the OTP via SMS
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_='+13203027585',
        to=phone_number
    )

    return otp


def login_otp(request):

    email = request.session.get('email')
    phone_number = request.session.get('phone_number')
    if email or phone_number:
        return redirect('store:store')
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            # country_code = form.cleaned_data['country_code']
            full_phone_number = str('+') + str(91) + phone_number
            request.session['phone_number'] = phone_number

            # Send the OTP
            otp = send_otp(full_phone_number)
            request.session['otp'] = otp

            # Render the OTP verification form
            form = OTPVerificationForm()

            context = {
                'form': form,
            }
            return render(request, 'accounts/otp.html', context)
    else:
        form = OTPForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/otplogin.html', context)


def verify_otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            # Verify the OTP
            if str(otp) == str(request.session['otp']):
                phone_number = request.session['phone_number']

                # Authenticate and log in the user
                user = auth.authenticate(phone_number=phone_number)

                if user is not None:
                    auth.login(request, user)
                    
                    return redirect('store:store')
                    messages.success(request, "You have been logged in!")
                else:
                    messages.error(request, "Something went wrong!")
            else:
                messages.error(request, "Invalid OTP!")
    else:
        form = OTPVerificationForm()

    context = {
        'form': form,
    }
    return render(request, 'signin_otp_submit.html', context)


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        
        return redirect('store:store')
    
