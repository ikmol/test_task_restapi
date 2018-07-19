from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAPIManager(BaseUserManager):
    """User API manager"""
    def create_user(self, email, name, lastname, password=None):
        """Create new user API"""
        if not email:
            raise ValueError("Incorrect email !")
        email = self.normalize_email(email)
        user = self.model(email=email,name=name,lastname=lastname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, lastname, password):
        
        user = self.create_user(email, name, lastname, password)
        user.is_superuser = True
        user.is_staff = True
        
        user.save(using=self._db)
        return user

class UserAPI(AbstractBaseUser,PermissionsMixin):
    """
    Create custom user for API
    """
    email = models.EmailField(max_length = 255, unique = True)
    name = models.CharField(max_length = 255, unique=True)
    lastname = models.CharField(max_length = 255)
    ether_address = models.CharField(max_length = 255)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","lastname"]

    objects = UserAPIManager()

    def get_full_name(self):
        full_name = self.name + ' ' + self.lastname
        return full_name
    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.name



