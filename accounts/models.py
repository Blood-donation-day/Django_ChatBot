from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from core.models import TimestampedModel
from django.db.models.signals import post_save
from django.dispatch import receiver
class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None):

        if email == None:
            raise TypeError('이메일 필수값입니다.')
        if password is None:
            raise TypeError('비밀번호는 필수값입니다.')
        
        user = self.model(
            email = self.normalize_email(email),
        )
        
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, password):
        
        user = self.create_user(email, password)
        
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        return user

class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    
    email = models.EmailField(max_length=100, db_index=True, unique=True)
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.profile.username:
            return self.profile.username
        return None


class Profile(TimestampedModel):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=20, blank=True)
    profile_img = models.ImageField(upload_to='accounts/profile_imgs', blank=True)
    introduce = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.user.email