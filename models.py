from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    is_shop_owner = models.BooleanField(_('Shop Owner'), default=False)
    is_staff = models.BooleanField(_('Staff Member'), default=False)
    is_active = models.BooleanField(_('Active'), default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_img = models.ImageField(upload_to='profile_images/', default=False)
    address = models.TextField(blank=False)
    mobile = models.CharField(max_length=12)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return self.first_name

class ShopOwnerManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_shop_owner=True)

class ShopOwner(CustomUser):
    class Meta:
        proxy = True

    objects = ShopOwnerManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_shop_owner = True
        return super().save(*args, **kwargs)