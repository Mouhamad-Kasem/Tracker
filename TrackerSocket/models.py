from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    
class Device(models.Model):
    IMEI = models.IntegerField(primary_key=True)
    license_plate = models.IntegerField()
    car_type = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True)
    company_id = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    descreption = models.TextField()
    
class Movement(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('paused', 'Paused'),
    )
    
    longitude = models.FloatField()
    latitude = models.FloatField()
    device_imei = models.ForeignKey(Device, on_delete=models.PROTECT)
    time_stamp = models.DateTimeField(auto_now_add=True)  
    speed = models.FloatField()
    status = models.CharField(max_length=10)
    
class Event(models.Model):
    type = models.CharField(max_length=100)
    movement_id = models.ForeignKey(Movement, on_delete=models.PROTECT)
    
    
#* Create Custom User Model
class CustomUserManager(UserManager):
    def _create_user(self, email, password, ** extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email.")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    company_id = models.IntegerField()
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    
    