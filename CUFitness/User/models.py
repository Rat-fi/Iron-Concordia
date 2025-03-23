from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now, timedelta

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_verified=False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """Create and return a superuser with full permissions."""
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True 
        user.is_verified = True
        user.save(using=self._db)
        return user

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    verification_token = models.CharField(max_length=64, blank=True, null=True)
    verification_expires = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()  # Assign the custom manager

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def generate_verification_token(self):
        print("generate_verification_token function called!")  # Debugging
        """Generate a new verification token and expiration time."""
        self.verification_token = get_random_string(length=64)
        self.verification_expires = now() + timedelta(minutes=30)
        self.save()
