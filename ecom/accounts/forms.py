from django import forms

class OTPForm(forms.Form):
    phone_number = forms.CharField( max_length=10, required=True)

class OTPVerificationForm(forms.Form):
    otp=forms.CharField(max_length=6)