from django.contrib.auth.backends import BaseBackend
from .models import Account


class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, **kwargs):
        try:
            user = Account.objects.get(phone_number=phone_number)
        except Account.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None