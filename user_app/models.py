from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number field must be set')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)

class UserData(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    email_address = models.EmailField(blank=True, null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number

    # If you need a method to check if the user is active, implement it here
    def is_active(self):
        return True  # Or use a condition based on your requirements

    # If you need a method to check if the user is a superuser, implement it here
    def is_superuser(self):
        return False  # Or use a condition based on your requirements

    # If you need a method to check user permissions, implement it here
    def has_perm(self, perm, obj=None):
        return True  # Or use a condition based on your requirements

    # If you need a method to check user permissions for a specific app, implement it here
    def has_module_perms(self, app_label):
        return True  # Or use a condition based on your requirements

    # Add or change the related_name for the groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Change this to a unique name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Change this to a unique name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )