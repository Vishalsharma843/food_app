from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator,validate_email
from django.contrib.auth.models import UserManager
from django.db import models
from .choices import *
# Create your models here.

phone_regex = RegexValidator(
    regex=r"^\d{10}", message="Phone number must be 10 digits only."
)

class UserManger(BaseUserManager):

    def create_user(self,phone_number):#password=None
        if not phone_number:
            raise ValueError("Users Must Have a Phone Number")
        user = self.model(phone_number=phone_number)
        # user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

class UserModel(AbstractBaseUser,PermissionsMixin):

    phone_number = models.CharField(unique=True, max_length=10, null=False, blank=False, validators=[phone_regex])
    # email = models.EmailField(max_length=50,blank=True,null= True,validators=[validate_email])
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField(blank=True,null=True)
    max_otp_try = models.CharField(max_length=2,default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    user_registered_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"
    
    objects = UserManger()
    def __str__(self):
        return self.phone_number
    

class UserProfile(models.Model):
    user_name = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg',upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f'{self.user_name} UserProfile'


# class UserBasicDetails(models.Model):
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     age = models.IntegerField(default=0)
#     gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True, blank=True)
#     email = models.EmailField(max_length=255, unique=True)
#     dob = models.DateField(null=True, blank=True)
#     image = models.ImageField(null=True, blank=True)

#     def __str__(self):
#         return self.first_name
    


# class Question(models.Model):
#     user=models.ForeignKey(UserBasicDetails, to_field = "email",null=True, blank=True,on_delete=models.CASCADE)
#     title = models.CharField(max_length=60)
#     slug = models.SlugField(unique=True,max_length=200)

# class Answer(models.Model):
#     user=models.ForeignKey(UserBasicDetails, to_field = "email",null=True, blank=True,on_delete=models.CASCADE)
#     answer = models.TextField()
#     post = models.ForeignKey(Question,on_delete=models.CASCADE)
    