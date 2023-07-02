from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField



# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, password=None):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        email = email.lower()
        # if not username:
        #     raise ValueError('User must have an username')

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number
           
           
        )

        user.set_password(password)
        user.save(using=self._db)
        user.is_active = False
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, password):
        user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            phone_number=phone_number,
            password = password,
            
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser, PermissionsMixin):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = PhoneNumberField()
    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superuser   = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name', 'last_name', 'phone_number']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return self.is_staff

    # def has_module_perms(self, add_label):
    #     return True
    
